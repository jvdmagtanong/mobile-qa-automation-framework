#!/usr/bin/env bash
set -e

echo "===== Ensuring Working Directories Exist ====="
mkdir -p test-reports
mkdir -p test-reports/allure-results

echo "===== Emulator Status Check ====="
echo "--- Boot Status ---"
adb shell getprop sys.boot_completed

echo "===== Optimizing UI System Configuration ====="
# Forces OS alerts/crashes to stay quiet so they don't block Appium's driver layers
adb shell settings put global hide_error_dialogs 1 || true
adb shell settings put global window_animation_scale 0.0 || true
adb shell settings put global transition_animation_scale 0.0 || true
adb shell settings put global animator_duration_scale 0.0 || true

echo "===== Installing Appium & Driver ====="
npm install -g appium@2
# Forces Appium 2 to install a legacy-compatible v2 major driver branch
appium driver install uiautomator2@4.2.9

echo "===== Initializing Appium Server Structure ====="
appium --address 127.0.0.1 --port 4723 --log-level debug > /tmp/appium.log 2>&1 &

echo "===== Waiting for Appium Port (4723) to Accept Connections ====="
for i in {1..15}; do
    if curl -sf "http://127.0.0.1:4723/status" > /dev/null; then
        echo "Appium Server is up and responding!"
        break
    fi
    echo "Waiting for Appium service map... ($i/15)"
    sleep 2
done

echo "===== Running pytest Target Specs ====="
set +e
pytest tests/mobile/cart/logged_out_user -v --alluredir=test-reports/allure-results
TEST_EXIT_CODE=$?
set -e

echo "===== Consolidating Runtime Diagnostics ====="
cp /tmp/appium.log test-reports/appium.log || true

echo "--- Capturing Final Logcat Snapshot ---"
# Only pulls down recent test-window buffers to prevent parsing failures or out-of-memory errors
adb logcat -d | grep -iE "ANR|systemui|not responding|Accessibility|UiAutomator|FATAL EXCEPTION|AndroidRuntime" > test-reports/ui-errors.txt || true
adb logcat -d > test-reports/logcat.txt || true

echo "===== Workflow Diagnostics Complete ====="
exit "$TEST_EXIT_CODE"
