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

echo "===== Pre-installing Appium Settings Helper ====="
# Find and pre-install the settings APK provided by the driver
SETTINGS_APK=$(find /home/runner/.appium -name "settings_apk-debug.apk" | head -n 1)
if [ -n "$SETTINGS_APK" ]; then
  adb install -r -g "$SETTINGS_APK" || true
fi

echo "===== Running mobile test ====="
pytest tests/mobile/authentication/test_login_successful.py -v --alluredir=test-reports/allure-results || true

TEST_EXIT_CODE=$?

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

echo "===== Appium log ====="
cat /tmp/appium.log || true

exit "$TEST_EXIT_CODE"