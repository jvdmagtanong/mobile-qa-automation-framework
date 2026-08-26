#!/bin/bash

AVD_NAME="${AVD_NAME:-Pixel_10}"

echo "Checking if Android emulator is already running..."

if adb devices | grep -q "emulator-.*device$"; then

    echo "Android emulator is already running."

else

    echo "Starting Android emulator: $AVD_NAME"

    emulator -avd "$AVD_NAME" -no-snapshot -no-boot-anim &

fi

echo "Waiting for Android emulator..."

adb wait-for-device

echo "Waiting for Android to finish booting..."

until adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r' | grep -q "1"; do
    sleep 2
done

echo "Android emulator is fully booted and ready."