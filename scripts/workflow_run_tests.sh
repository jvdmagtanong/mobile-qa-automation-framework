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

sleep 5

echo "===== Cleaning Prior UiAutomator2 Server Packages ====="
adb uninstall io.appium.uiautomator2.server || true
adb uninstall io.appium.uiautomator2.server.test || true

echo "===== Disabling System Animations & Crash Dialogs ====="
adb shell settings put global hide_error_dialogs 1 || true
adb shell settings put global show_mute_in_crash_dialog 0 || true
adb shell settings put global window_animation_scale 0.0 || true
adb shell settings put global transition_animation_scale 0.0 || true
adb shell settings put global animator_duration_scale 0.0 || true

# Grant background permission to prevent settings app blockages
adb shell pm grant io.appium.settings android.permission.SET_ANIMATION_SCALE || true

echo "===== Installing Appium & Driver ====="
npm install -g appium@3
appium driver install uiautomator2

echo "===== Starting Appium server ====="
appium --address 127.0.0.1 --port 4723 --log-level debug > /tmp/appium.log 2>&1 &

sleep 5
curl -sf "http://127.0.0.1:4723/status"

echo "===== Running Mobile Test ====="
set +e
pytest tests/mobile/authentication/test_login_successful.py -v --alluredir=test-reports/allure-results
TEST_EXIT_CODE=$?
set -e

echo "===== Appium log ====="
cat /tmp/appium.log || true

exit "$TEST_EXIT_CODE"