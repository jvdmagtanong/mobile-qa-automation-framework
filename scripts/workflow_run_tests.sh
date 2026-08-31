#!/usr/bin/env bash
set -e

echo "===== Waiting for Full Boot Completion ====="
until [ "$(adb shell getprop sys.boot_completed | tr -d '\r')" = "1" ]; do
  echo "Waiting for sys.boot_completed..."
  sleep 3
done

echo "===== Waiting for Package Manager Service to Settle ====="
# Check that the system package manager daemon actively responds to IPC calls
until adb shell pm path android > /dev/null 2>&1; do
  echo "Package Manager service starting up..."
  sleep 3
done

# Extra buffer to let background system services bind IPC sockets
sleep 5

echo "===== Cleaning Prior UiAutomator2 Server Packages ====="
adb uninstall io.appium.uiautomator2.server || true
adb uninstall io.appium.uiautomator2.server.test || true

echo "===== Disabling and Suppressing System Settings & ANR Dialogs ====="
adb shell settings put global hide_error_dialogs 1 || true
adb shell settings put global show_mute_in_crash_dialog 0 || true

# Force-stop settings and restart System UI cleanly
adb shell am force-stop com.android.settings || true
adb shell am force-stop com.android.systemui || true
sleep 2

# Dismiss any active system popups
adb shell input keyevent 66 || true
adb shell input keyevent 4 || true

echo "===== Verifying Page Size ====="
adb shell getconf PAGE_SIZE || true

echo "===== Disabling Animations Safely ====="
adb shell settings put global window_animation_scale 0.0 || true
adb shell settings put global transition_animation_scale 0.0 || true
adb shell settings put global animator_duration_scale 0.0 || true

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

echo "===== Pre-installing Appium Settings Helper ====="
SETTINGS_APK=$(find /home/runner/.appium -name "settings_apk-debug.apk" 2>/dev/null | head -n 1)
if [ -n "$SETTINGS_APK" ]; then
  adb install -r -g "$SETTINGS_APK" || true
fi

echo "===== Pre-clearing App State ====="
adb shell am force-stop com.saucelabs.mydemoapp.android || true
sleep 2

echo "===== Starting Background System UI Watchdog ====="
(
  while true; do
    adb shell uiautomator dump /sdcard/window_dump.xml > /dev/null 2>&1 || true
    if adb shell cat /sdcard/window_dump.xml 2>/dev/null | grep -q "System UI isn't responding"; then
      echo "===== Detected System UI ANR Dialog - Dismissing ====="
      adb shell input keyevent 61 || true
      adb shell input keyevent 66 || true
    fi
    sleep 3
  done
) &
WATCHDOG_PID=$!

echo "===== Running Mobile Test ====="
set +e
pytest tests/mobile/authentication/test_login_successful.py -v --alluredir=test-reports/allure-results
TEST_EXIT_CODE=$?
set -e

# Stop watchdog background loop
kill $WATCHDOG_PID || true

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