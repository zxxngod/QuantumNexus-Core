#!/bin/bash

# Set strict mode
set -euo pipefail

# Constants
LOG_FILE="test_results.log"
TEST_DIR="tests"
PYTHON_TEST_CMD="python3 -m unittest discover -s $TEST_DIR -p 'test_*.py'"
NODE_TEST_CMD="npm test"

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Function to run Python tests
run_python_tests() {
    log "Running Python tests..."
    if command -v python3 >/dev/null 2>&1; then
        eval "$PYTHON_TEST_CMD" | tee -a "$LOG_FILE"
    else
        log "Python3 is not installed. Please install Python3 and try again."
        exit 1
    fi
}

# Function to run Node.js tests
run_node_tests() {
    log "Running Node.js tests..."
    if command -v npm >/dev/null 2>&1; then
        eval "$NODE_TEST_CMD" | tee -a "$LOG_FILE"
    else
        log "npm is not installed. Please install npm and try again."
        exit 1
    fi
}

# Function to summarize test results
summarize_results() {
    log "Summarizing test results..."
    if grep -q "FAILED" "$LOG_FILE"; then
        log "Some tests failed. Please check the log for details."
        exit 1
    else
        log "All tests passed successfully!"
    fi
}

# Main script execution
log "Starting test execution..."

# Create or clear the log file
: > "$LOG_FILE"

# Run tests
run_python_tests
run_node_tests

# Summarize results
summarize_results

log "Test execution completed!"
