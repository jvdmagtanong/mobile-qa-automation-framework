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
adb shell settings put global hide_error_dialogs 1 || true
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

echo "===== Emulator Architecture ====="
adb shell getprop ro.product.cpu.abi
adb shell getprop ro.product.cpu.abilist
adb shell getprop ro.product.device
adb shell getprop ro.product.name
adb shell getprop ro.kernel.qemu.avd_name

echo "===== Emulator Graphics ====="
adb shell getprop ro.kernel.qemu.uirenderer
adb shell getprop debug.hwui.renderer

echo "===== Emulator Memory ====="
adb shell cat /proc/meminfo | head -10
adb logcat -c

echo "===== Running Mobile Test ====="
set +e
pytest tests/mobile/cart/logged_in_user/ -v --alluredir=test-reports/allure-results
TEST_EXIT_CODE=$?
set -e

echo "===== Android ANR / Crash Evidence ====="
adb logcat -d | grep -iE "ANR|systemui|not responding|FATAL EXCEPTION|AndroidRuntime" || true
adb logcat -d > test-reports/logcat.txt
grep -iE "ANR|systemui|not responding|FATAL EXCEPTION" test-reports/logcat.txt || true


echo "===== Appium log ====="
cat /tmp/appium.log || true

exit "$TEST_EXIT_CODE"