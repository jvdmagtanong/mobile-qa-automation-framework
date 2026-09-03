#!/usr/bin/env bash
set -e

echo "===== Waiting for Full Boot Completion ====="
until [ "$(adb shell getprop sys.boot_completed | tr -d '\r')" = "1" ]; do
  echo "Waiting for sys.boot_completed..."
  sleep 3
done

echo "===== Waiting for Package Manager Service to Settle ====="
until adb shell pm path android > /dev/null 2>&1; do
  echo "Package Manager service starting up..."
  sleep 3
done

sleep 10

echo "===== Cleaning Up Old UiAutomator2 Server Binaries ====="
adb uninstall io.appium.uiautomator2.server || true
adb uninstall io.appium.uiautomator2.server.test || true

echo "===== Disabling System Animations ====="
# adb shell settings put global hide_error_dialogs 1 || true
adb shell settings put global window_animation_scale 0.0 || true
adb shell settings put global transition_animation_scale 0.0 || true
adb shell settings put global animator_duration_scale 0.0 || true

echo "===== Installing Appium & Driver ====="
npm install -g appium@3
appium driver install uiautomator2

echo "===== Starting Appium server ====="
appium --address 127.0.0.1 --port 4723 --log-level debug > /tmp/appium.log 2>&1 &

sleep 5
curl -sf "http://127.0.0.1:4723/status"

mkdir -p test-reports

echo "===== Starting Memory Monitor ====="

(
  while true; do
    echo "===== $(date) ====="
    adb shell cat /proc/meminfo | grep -E "MemTotal|MemAvailable|MemFree|SwapFree"
    sleep 10
  done
) > test-reports/memory.log 2>&1 &

MEMORY_MONITOR_PID=$!

echo "===== Running Mobile Test ====="
set +e
pytest tests/mobile/cart/logged_out_user -v --alluredir=test-reports/allure-results
TEST_EXIT_CODE=$?
set -e

kill "$MEMORY_MONITOR_PID" || true

echo "===== Appium log ====="
cat /tmp/appium.log || true
cp /tmp/appium.log test-reports/appium.log || true

echo "===== Post-Test UI State ====="

echo "--- Current Activity ---"
adb shell dumpsys activity activities | grep -E "mResumedActivity|mFocusedApp" || true

echo "--- App Process ---"
adb shell pidof com.saucelabs.mydemoapp.android || true

echo "--- System UI Process ---"
adb shell pidof com.android.systemui || true

echo "--- Accessibility Services ---"
adb shell settings get secure enabled_accessibility_services || true

echo "--- Accessibility Manager ---"
adb shell dumpsys accessibility > test-reports/accessibility.txt || true

echo "--- UI / ANR Errors ---"
adb logcat -d | grep -iE \
"ANR|systemui|not responding|Accessibility|UiAutomator|FATAL EXCEPTION|AndroidRuntime" \
> test-reports/ui-errors.txt || true

echo "--- Full Logcat ---"
adb logcat -d > test-reports/logcat.txt

exit "$TEST_EXIT_CODE"