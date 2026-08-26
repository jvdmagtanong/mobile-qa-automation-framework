#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "========================================"
echo "Starting mobile test environment"
echo "========================================"
echo ""

echo "Starting Android emulator..."

"$PROJECT_ROOT/scripts/start_emulator.sh"

echo ""

echo "Starting Appium server..."

"$PROJECT_ROOT/scripts/start_appium.sh"

echo ""

echo "========================================"
echo "Mobile test environment is ready!"
echo "========================================"