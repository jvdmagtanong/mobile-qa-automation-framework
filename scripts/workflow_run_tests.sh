#!/usr/bin/env bash
set -e

echo "===== workflow_run_tests.sh STARTED ====="

BOOT_TIMEOUT=90
PM_TIMEOUT=90
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
# Step 4: Wait for Package Manager
# ============================================================

echo "===== Step 4: Waiting for Package Manager ====="

for i in $(seq 1 30); do
    if timeout 10s adb shell pm path android >/dev/null 2>&1; then
        echo "Package Manager is ready."
        break
    fi

    echo "Waiting for Package Manager... ($((i * 3))s/$PM_TIMEOUT"s")"
    sleep 3
done

if ! timeout 10s adb shell pm path android >/dev/null 2>&1; then
    echo "ERROR: Package Manager did not become ready."

    echo "===== Android Diagnostics ====="
    adb devices || true
    adb shell service check package || true
    adb shell service check settings || true
    adb shell service check activity || true
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
# Step 6: Install Appium
# ============================================================

echo "===== Step 6: Installing Appium ====="
npm install -g appium@3
appium driver install uiautomator2

echo "Appium version:"
appium --version

echo "Installed drivers:"
appium driver list --installed

SETTINGS_APK="$HOME/.appium/node_modules/appium-uiautomator2-driver/node_modules/io.appium.settings/apks/settings_apk-debug.apk"

echo "===== Testing Appium Settings APK Installation ====="

timeout 60s adb -s emulator-5554 install -g "$SETTINGS_APK"

# ============================================================
# Step 7: Start Appium
# ============================================================

echo "===== Step 7: Starting Appium ====="

rm -f /tmp/appium.log

appium \
    --address 127.0.0.1 \
    --port 4723 \
    --log-level debug \
    > /tmp/appium.log 2>&1 &

APPIUM_PID=$!

echo "Appium PID: $APPIUM_PID"

# ============================================================
# Step 8: Wait for Appium
# ============================================================

echo "===== Step 8: Waiting for Appium ====="

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

echo "===== Android Framework Health Check ====="

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
# Step 9: Run Tests
# ============================================================

echo "===== Step 9: Running Tests ====="

mkdir -p test-reports/allure-results

set +e

pytest \
    tests/mobile/cart/logged_out_user \
    -v \
    --alluredir=test-reports/allure-results

TEST_EXIT_CODE=$?

set -e

echo "Pytest exit code: $TEST_EXIT_CODE"

# ============================================================
# Step 10: Diagnostics
# ============================================================

echo "===== Step 10: Collecting Diagnostics ====="
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