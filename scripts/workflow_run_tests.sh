```bash
#!/usr/bin/env bash
set -e

# ============================================================
# Configuration
# ============================================================

ANDROID_SERVICE_TIMEOUT=90
APPIUM_TIMEOUT=30

# ============================================================
# Helper: wait for Android service
# ============================================================

wait_for_service() {
    local service_name="$1"
    local timeout="$2"
    local elapsed=0

    echo "===== Waiting for Android service: $service_name ====="
    while [ "$elapsed" -lt "$timeout" ]; do
        if adb shell service check "$service_name" 2>/dev/null | grep -q "found"; then
            echo "Android service '$service_name' is ready."
            return 0
        fi
        echo "Waiting for '$service_name'... (${elapsed}s/${timeout}s)"
        sleep 3
        elapsed=$((elapsed + 3))
    done

    echo "ERROR: Android service '$service_name' did not become ready within ${timeout}s."
    echo "===== Android Service Diagnostics ====="
    adb devices || true
    adb shell getprop sys.boot_completed || true
    adb shell getprop dev.bootcomplete || true
    adb shell service check "$service_name" || true

    return 1
}

# ============================================================
# Wait for Android device
# ============================================================

echo "===== Waiting for Android Emulator ====="
adb wait-for-device
echo "Android device detected."

# ============================================================
# Wait for Android boot
# ============================================================

echo "===== Waiting for Android Boot Completion ====="
boot_timeout=90
elapsed=0

while [ "$elapsed" -lt "$boot_timeout" ]; do
    boot_completed=$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')
    if [ "$boot_completed" = "1" ]; then
        echo "Android boot completed."
        break
    fi
    echo "Waiting for Android boot... (${elapsed}s/${boot_timeout}s)"
    sleep 3
    elapsed=$((elapsed + 3))
done

if [ "$boot_completed" != "1" ]; then
    echo "ERROR: Android did not finish booting within ${boot_timeout}s."
    echo "===== Boot Diagnostics ====="
    adb devices || true
    adb shell getprop sys.boot_completed || true
    adb shell getprop dev.bootcomplete || true
    adb shell getprop ro.build.version.sdk || true

    exit 1
fi

# ============================================================
# Verify critical Android framework services
# ============================================================

echo "===== Verifying Core Android Service Readiness ====="
# Package Manager
echo "===== Checking Package Manager ====="
pm_timeout=90
elapsed=0

while [ "$elapsed" -lt "$pm_timeout" ]; do
    if adb shell pm path android >/dev/null 2>&1; then
        echo "Package Manager is ready."
        break
    fi
    echo "Waiting for Package Manager... (${elapsed}s/${pm_timeout}s)"
    sleep 3
    elapsed=$((elapsed + 3))
done

if ! adb shell pm path android >/dev/null 2>&1; then
    echo "ERROR: Package Manager did not become ready."
    adb shell pm path android || true
    adb shell service list | head -100 || true

    exit 1
fi

# Settings
wait_for_service "settings" "$ANDROID_SERVICE_TIMEOUT"

# Activity Manager
wait_for_service "activity" "$ANDROID_SERVICE_TIMEOUT"

# ============================================================
# Verify framework is actually responding
# ============================================================

echo "===== Performing Android Framework Health Check ====="
if ! adb shell cmd settings get global adb_enabled >/dev/null 2>&1; then
    echo "ERROR: Settings service is present but not responding correctly."
    adb shell service check settings || true
    exit 1
fi

if ! adb shell dumpsys activity activities >/dev/null 2>&1; then
    echo "ERROR: Activity Manager is present but not responding correctly."
    adb shell service check activity || true
    exit 1
fi

echo "Android framework health check passed."

# ============================================================
# Configure Android
# ============================================================

echo "===== Optimizing UI System Configuration ====="
adb shell settings put global hide_error_dialogs 1
adb shell settings put global window_animation_scale 0.0
adb shell settings put global transition_animation_scale 0.0
adb shell settings put global animator_duration_scale 0.0

echo "Android UI configuration applied successfully."

# ============================================================
# Working directories
# ============================================================

echo "===== Ensuring Working Directories Exist ====="
mkdir -p test-reports
mkdir -p test-reports/allure-results

# ============================================================
# Emulator status
# ============================================================

echo "===== Emulator Status Check ====="
echo "--- Devices ---"
adb devices
echo "--- Boot Status ---"
adb shell getprop sys.boot_completed
echo "--- Android Version ---"
adb shell getprop ro.build.version.release
echo "--- API Level ---"
adb shell getprop ro.build.version.sdk
echo "--- Architecture ---"
adb shell getprop ro.product.cpu.abi

# ============================================================
# Install Appium
# ============================================================
echo "===== Installing Appium & Driver ====="
npm install -g appium@2
appium driver install uiautomator2
echo "===== Appium Version ====="
appium --version
echo "===== UiAutomator2 Driver ====="
appium driver list --installed

# ============================================================
# Start Appium
# ============================================================

echo "===== Starting Appium Server ====="
rm -f /tmp/appium.log
appium \
    --address 127.0.0.1 \
    --port 4723 \
    --log-level debug \
    > /tmp/appium.log 2>&1 &

APPIUM_PID=$!

echo "Appium PID: $APPIUM_PID"

# ============================================================
# Wait for Appium
# ============================================================
echo "===== Waiting for Appium Port (4723) ====="
appium_ready=false

for i in $(seq 1 "$APPIUM_TIMEOUT"); do
    if ! kill -0 "$APPIUM_PID" 2>/dev/null; then
        echo "ERROR: Appium process exited unexpectedly."
        echo "===== Appium Log ====="
        cat /tmp/appium.log || true

        exit 1
    fi
    if curl -sf "http://127.0.0.1:4723/status" >/dev/null; then
        echo "Appium Server is up and responding!"
        appium_ready=true
        break
    fi
    echo "Waiting for Appium... ($i/${APPIUM_TIMEOUT}s)"
    sleep 1
done

if [ "$appium_ready" != true ]; then
    echo "ERROR: Appium did not become ready within ${APPIUM_TIMEOUT}s."
    echo "===== Appium Log ====="
    cat /tmp/appium.log || true

    exit 1
fi

# ============================================================
# Run Tests
# ============================================================
echo "===== Running pytest Target Specs ====="

set +e

pytest \
    tests/mobile/cart/logged_out_user \
    -v \
    --alluredir=test-reports/allure-results

TEST_EXIT_CODE=$?

set -e

echo "===== pytest Exit Code: $TEST_EXIT_CODE ====="

# ============================================================
# Diagnostics
# ============================================================

echo "===== Consolidating Runtime Diagnostics ====="
cp /tmp/appium.log test-reports/appium.log || true
echo "--- Capturing Android Diagnostics ---"
adb devices > test-reports/adb-devices.txt || true
adb shell getprop > test-reports/getprop.txt || true
echo "--- Capturing UI/System Errors ---"
adb logcat -d \
    | grep -iE \
      "ANR|systemui|not responding|Accessibility|UiAutomator|FATAL EXCEPTION|AndroidRuntime" \
    > test-reports/ui-errors.txt || true
echo "--- Capturing Full Logcat ---"
adb logcat -d > test-reports/logcat.txt || true
echo "===== Workflow Diagnostics Complete ====="

exit "$TEST_EXIT_CODE"
```
