#!/usr/bin/env bash
set -e

echo "===== workflow_run_tests.sh STARTED ====="
mkdir -p test-reports
BOOT_TIMEOUT=90
APPIUM_TIMEOUT=30

echo "============================================================"
echo "Mobile Test Environment"
echo "============================================================"

# ============================================================
# Step 1: KVM Check
# ============================================================

echo "===== Step 1: KVM Virtualization Check ====="

if [ -r /dev/kvm ] && [ -w /dev/kvm ]; then
    echo "SUCCESS: KVM hardware acceleration is available."
else
    echo "WARNING: KVM is not available."
fi

# ============================================================
# Step 2: Wait for Emulator
# ============================================================

echo "===== Step 2: Waiting for Android Emulator ====="

for i in $(seq 1 30); do
    if adb devices | grep -q "emulator-5554.*device"; then
        echo "Android emulator detected."
        break
    fi

    echo "Waiting for emulator... ($i/30)"
    sleep 2
done

if ! adb devices | grep -q "emulator-5554.*device"; then
    echo "ERROR: Android emulator did not become available."
    adb devices || true
    exit 1
fi

# ============================================================
# Step 3: Wait for Android Boot
# ============================================================

echo "===== Step 3: Waiting for Android Boot ====="

for i in $(seq 1 30); do
    if [ "$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')" = "1" ]; then
        echo "Android boot completed."
        break
    fi

    echo "Waiting for Android boot... ($((i * 3))s/$BOOT_TIMEOUT"s")"
    sleep 3
done

if [ "$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')" != "1" ]; then
    echo "ERROR: Android boot did not complete."
    adb shell getprop sys.boot_completed || true
    exit 1
fi

# ============================================================
# Step 4: Wait for Android Framework Services
# ============================================================

echo "===== Step 4: Waiting for Android Framework Services ====="
FRAMEWORK_TIMEOUT=120
FRAMEWORK_READY_COUNT=0

for i in $(seq 1 "$FRAMEWORK_TIMEOUT"); do
    PACKAGE_SERVICE="$(adb shell service check package 2>/dev/null | tr -d '\r')"
    SETTINGS_SERVICE="$(adb shell service check settings 2>/dev/null | tr -d '\r')"
    ACTIVITY_SERVICE="$(adb shell service check activity 2>/dev/null | tr -d '\r')"

    if [[ "$PACKAGE_SERVICE" == "Service package: found" ]] && \
       [[ "$SETTINGS_SERVICE" == "Service settings: found" ]] && \
       [[ "$ACTIVITY_SERVICE" == "Service activity: found" ]]; then
        FRAMEWORK_READY_COUNT=$((FRAMEWORK_READY_COUNT + 1))
        echo "Framework services ready: $FRAMEWORK_READY_COUNT/3"

        if [ "$FRAMEWORK_READY_COUNT" -ge 3 ]; then
            echo "SUCCESS: Android framework services are ready and stable."
            break
        fi
    else
        FRAMEWORK_READY_COUNT=0
        echo "Waiting for Android framework services... ($i/${FRAMEWORK_TIMEOUT}s)"
    fi

    sleep 1
done

if [ "$FRAMEWORK_READY_COUNT" -lt 3 ]; then
    echo "ERROR: Android framework services did not become stable."
    echo "===== Android Diagnostics ====="
    adb devices || true
    adb shell service check package || true
    adb shell service check settings || true
    adb shell service check activity || true
    adb shell pidof system_server || true
    adb shell getprop sys.boot_completed || true
    exit 1
fi

# ============================================================
# Step 5: SystemUI Check
# ============================================================

echo "===== Step 5: Checking SystemUI ====="

if adb shell pidof com.android.systemui >/dev/null 2>&1; then
    echo "SystemUI is running."
else
    echo "WARNING: SystemUI process not detected."
fi

# ============================================================
# Step 6: Capture Android Framework Logs
# ============================================================
echo "===== Step 6: Starting Android Logcat Capture ====="
rm -f test-reports/logcat-framework.txt
adb logcat -c || true
adb -s emulator-5554 logcat -b all -v threadtime > test-reports/logcat-framework.txt 2>&1 &
LOGCAT_PID=$!
echo "Logcat PID: $LOGCAT_PID"

# ============================================================
# Step 7: Install Appium
# ============================================================

echo "===== Step 7: Installing Appium ====="
npm install -g appium@3
appium driver install uiautomator2

echo "Appium version:"
appium --version

echo "Installed drivers:"
appium driver list --installed

# ============================================================
# Step 8: Start Appium
# ============================================================

echo "===== Step 8: Starting Appium ====="

rm -f /tmp/appium.log

appium \
    --address 127.0.0.1 \
    --port 4723 \
    --log-level debug \
    > /tmp/appium.log 2>&1 &

APPIUM_PID=$!
echo "Appium PID: $APPIUM_PID"

# ============================================================
# Step 9: Wait for Appium
# ============================================================

echo "===== Step 9: Waiting for Appium ====="

appium_ready=false

for i in $(seq 1 "$APPIUM_TIMEOUT"); do
    if ! kill -0 "$APPIUM_PID" 2>/dev/null; then
        echo "ERROR: Appium exited unexpectedly."
        cat /tmp/appium.log || true
        exit 1
    fi

    if curl -sf "http://127.0.0.1:4723/status" >/dev/null; then
        echo "Appium is ready."
        appium_ready=true
        break
    fi

    echo "Waiting for Appium... ($i/${APPIUM_TIMEOUT}s)"
    sleep 1
done

if [ "$appium_ready" != true ]; then
    echo "ERROR: Appium did not become ready."
    echo "===== Appium Log ====="
    cat /tmp/appium.log || true
    exit 1
fi

# ============================================================
# Step 10: Android Framework Health Check
# ============================================================

echo "===== Step 10: Android Framework Health Check ====="
echo "Package Manager:"
adb shell service check package || true
echo "Activity Manager:"
adb shell service check activity || true
echo "Settings:"
adb shell service check settings || true
echo "System Server:"
adb shell pidof system_server || true
echo "System UI:"
adb shell pidof com.android.systemui || true
echo "Boot completed:"
adb shell getprop sys.boot_completed || true

# ============================================================
# Step 11: Run Tests
# ============================================================
echo "===== Step 11: Running Tests ====="

TEST_SUITE="${TEST_SUITE:-all}"

rm -rf test-reports/allure-results
mkdir -p test-reports/allure-results

cat > test-reports/allure-results/environment.properties <<EOF
Test Suite=$TEST_SUITE
Python=$(python --version 2>&1)
Appium=$(appium --version 2>&1)
Device=Pixel 2
Android=API 30
EOF

set +e

PYTEST_ARGS=(
    tests/mobile
    -v
    --alluredir=test-reports/allure-results
)

case "$TEST_SUITE" in
    smoke)
        echo "Test selection: SMOKE tests"
        PYTEST_ARGS+=(-m "smoke")
        ;;

    regression)
        echo "Test selection: REGRESSION tests"
        PYTEST_ARGS+=(-m "regression")
        ;;

    critical)
        echo "Test selection: CRITICAL tests"
        PYTEST_ARGS+=(-m "critical")
        ;;

    all)
        echo "Test selection: ALL tests"
        ;;

    *)
        echo "ERROR: Unknown TEST_SUITE: $TEST_SUITE"
        exit 1
        ;;
esac

pytest "${PYTEST_ARGS[@]}"

TEST_EXIT_CODE=$?

set -e

echo "Pytest exit code: $TEST_EXIT_CODE"

# ============================================================
# Step 12: Diagnostics
# ============================================================
echo "===== Step 12: Collecting Diagnostics ====="

if [[ -n "${LOGCAT_PID:-}" ]]; then
    kill "$LOGCAT_PID" 2>/dev/null || true
    wait "$LOGCAT_PID" 2>/dev/null || true
fi

echo "===== Appium Log ====="
cp /tmp/appium.log test-reports/appium.log || true
echo "===== ADB Devices ====="
adb devices > test-reports/adb-devices.txt || true
echo "===== Android Properties ====="
adb shell getprop > test-reports/getprop.txt || true
echo "===== Accessibility Diagnostics ====="
adb shell dumpsys accessibility > test-reports/accessibility.txt || true
echo "===== UI/System Errors ====="
adb logcat -d \
    | grep -iE \
      "ANR|systemui|not responding|Accessibility|UiAutomator|FATAL EXCEPTION|AndroidRuntime" \
    > test-reports/ui-errors.txt || true
echo "===== Full Logcat ====="
adb logcat -d > test-reports/logcat.txt || true
echo "===== System Monitor ====="
{
    echo "===== Date ====="
    date
    echo "===== Uptime ====="
    uptime
    echo "===== Memory ====="
    free -h
    echo "===== CPU ====="
    nproc
    echo "===== Processes ====="
    ps aux --sort=-%cpu | head -20
} > test-reports/system-monitor.log 2>&1 || true

echo "===== Final Android Framework Health Check ====="
adb shell service check package || true
adb shell service check activity || true
adb shell service check settings || true
adb shell pidof system_server || true
adb shell pidof com.android.systemui || true
adb shell getprop sys.boot_completed || true
echo "===== Workflow Diagnostics Complete ====="

echo "===== Workflow Complete ====="

exit "$TEST_EXIT_CODE"
