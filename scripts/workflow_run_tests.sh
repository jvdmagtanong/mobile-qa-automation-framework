#!/usr/bin/env bash
set -e

echo "===== Waiting for System Services and Package Manager ====="
until adb shell pm path android > /dev/null 2>&1; do
  echo "Waiting for Package Manager..."
  sleep 3
done

until [ "$(adb shell getprop sys.boot_completed | tr -d '\r')" = "1" ]; do
  echo "Waiting for full boot completion..."
  sleep 3
done

echo "===== Cleaning prior UiAutomator2 Server packages ====="
adb uninstall io.appium.uiautomator2.server || true
adb uninstall io.appium.uiautomator2.server.test || true

echo "===== Disabling and Suppressing System Settings & ANR Dialogs ====="
# Suppress error and ANR pop-ups globally
adb shell settings put global hide_error_dialogs 1
adb shell settings put global show_mute_in_crash_dialog 0

# Force-stop system settings process
adb shell am force-stop com.android.settings || true

# Force restart SystemUI to clear any stuck overlay frames
adb shell am force-stop com.android.systemui || true

# Wait 2 seconds for SystemUI to cleanly rebind without ANR dialogs
sleep 2

# Send keyevents to dismiss active modals
adb shell input keyevent 66 || true
adb shell input keyevent 4 || true

echo "===== Verifying Page Size ====="
adb shell getconf PAGE_SIZE

echo "===== Disabling Animations Safely ====="
adb shell settings put global window_animation_scale 0.0
adb shell settings put global transition_animation_scale 0.0
adb shell settings put global animator_duration_scale 0.0

echo "===== Installing Appium ====="
npm install -g appium@3
appium --version

echo "===== Installing UiAutomator2 driver ====="
appium driver install uiautomator2

echo "===== Starting Appium server ====="
appium --address 127.0.0.1 --port 4723 --log-level debug > /tmp/appium.log 2>&1 &

echo "Waiting for Appium server..."
sleep 5

echo "Checking Appium server..."
curl -sf "http://127.0.0.1:4723/status"
echo "Appium server is ready."

echo "===== Installing test APK safely ====="
# Wait an extra moment to ensure Package Manager service isn't busy
sleep 5
adb install -r -g --no-streaming "$APK_PATH"

# Start a background watchdog that clicks "Wait" on System UI dialogs if they pop up
(
  while true; do
    # Search for the "Wait" text or button on screen and tap it if present
    adb shell uiautomator dump /sdcard/window_dump.xml > /dev/null 2>&1 || true
    if adb shell cat /sdcard/window_dump.xml 2>/dev/null | grep -q "System UI isn't responding"; then
      echo "===== Detected System UI ANR Dialog - Clicking Wait ====="
      # Press TAB then ENTER to focus and click 'Wait'
      adb shell input keyevent 61
      adb shell input keyevent 66
    fi
    sleep 3
  done
) &
WATCHDOG_PID=$!

echo "===== Running mobile test ====="
pytest tests/mobile/authentication/test_login_successful.py -v --alluredir=test-reports/allure-results || true

TEST_EXIT_CODE=$?

# Kill watchdog when tests finish
kill $WATCHDOG_PID || true

echo "===== Appium log ====="
cat /tmp/appium.log || true

echo ""

if [ "$TEST_EXIT_CODE" -eq 0 ]; then
    echo "========================================"
    echo "All Tests Passed"
    echo "========================================"
else
    echo "========================================"
    echo "Some Tests Failed"
    echo "========================================"
fi

echo ""

exit "$TEST_EXIT_CODE"