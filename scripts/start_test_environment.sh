#!/bin/bash

echo "========================================"
echo "Starting mobile test environment"
echo "========================================"

echo ""
echo "Starting Android emulator..."
./scripts/start_emulator.sh

echo ""
echo "Starting Appium server..."
./scripts/start_appium.sh

echo ""
echo "========================================"
echo "Mobile test environment is ready!"
echo "========================================"

