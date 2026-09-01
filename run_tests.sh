#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ALLURE_RESULTS_DIR="$PROJECT_ROOT/test-reports/allure-results"
ALLURE_REPORT_DIR="$PROJECT_ROOT/test-reports/allure-report"

echo "========================================"
echo "Mobile QA Automation Test Runner"
echo "========================================"
echo ""

echo "Cleaning previous Allure results..."

rm -rf "$ALLURE_RESULTS_DIR"
rm -rf "$ALLURE_REPORT_DIR"

mkdir -p "$ALLURE_RESULTS_DIR"

echo "Allure directories cleaned."

echo ""
echo "Starting test environment..."

"$PROJECT_ROOT/scripts/start_test_environment.sh"

echo ""
echo "Mobile test environment is ready."

echo ""
echo "========================================"
echo "Running Tests"
echo "========================================"
echo ""

set +e

pytest tests/mobile/authentication/test_login*.py --alluredir="$ALLURE_RESULTS_DIR"

TEST_EXIT_CODE=$?

set -e

echo ""
echo "========================================"
echo "Generating Allure Report"
echo "========================================"
echo ""

allure generate \
    "$ALLURE_RESULTS_DIR" \
    -o "$ALLURE_REPORT_DIR" \
    --clean

echo ""
echo "Allure HTML report generated."
echo "Report: $ALLURE_REPORT_DIR"

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