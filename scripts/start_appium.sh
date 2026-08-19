#!/bin/bash

APPIUM_HOST="127.0.0.1"
APPIUM_PORT="4723"

echo "Checking if Appium server is already running..."

if curl -sf "http://${APPIUM_HOST}:${APPIUM_PORT}/status" > /dev/null; then
    echo "Appium server is already running."
    exit 0
fi

echo "Starting Appium server..."

appium --address "$APPIUM_HOST" --port "$APPIUM_PORT" > /tmp/appium.log 2>&1 &

echo "Waiting for Appium server..."

until curl -sf "http://${APPIUM_HOST}:${APPIUM_PORT}/status" > /dev/null; do
    sleep 1
done

echo "Appium server is ready."

