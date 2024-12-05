#!/bin/bash

# Set strict mode
set -euo pipefail

# Constants
REPO_URL="https://github.com/KOSASIH/QuantumNexus-Core.git"
DEPLOY_DIR="/opt/quantumnexus"
ENV_FILE=".env"
LOG_FILE="deploy.log"

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install dependencies
install_dependencies() {
    log "Installing dependencies..."
    if command_exists pip; then
        pip install -r requirements.txt
    else
        log "pip is not installed. Please install pip and try again."
        exit 1
    fi

    if command_exists npm; then
        npm install
    else
        log "npm is not installed. Please install npm and try again."
        exit 1
    fi
}

# Function to set up environment variables
setup_environment() {
    log "Setting up environment variables..."
    if [ -f "$ENV_FILE" ]; then
        export $(grep -v '^#' "$ENV_FILE" | xargs)
    else
        log "$ENV_FILE not found. Please create it with the necessary environment variables."
        exit 1
    fi
}

# Function to deploy smart contracts
deploy_smart_contracts() {
    log "Deploying smart contracts..."
    # Assuming you have a script to deploy contracts
    if command_exists truffle; then
        truffle migrate --network mainnet
    else
        log "Truffle is not installed. Please install Truffle and try again."
        exit 1
    fi
}

# Function to start the application
start_application() {
    log "Starting the application..."
    # Assuming you have a main application script
    if command_exists python; then
        python src/main.py &
    else
        log "Python is not installed. Please install Python and try again."
        exit 1
    fi
}

# Function to clean up old deployments
cleanup_old_deployments() {
    log "Cleaning up old deployments..."
    if [ -d "$DEPLOY_DIR" ]; then
        rm -rf "$DEPLOY_DIR"
    fi
}

# Main script execution
log "Starting deployment process..."

cleanup_old_deployments
mkdir -p "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

log "Cloning repository..."
git clone "$REPO_URL" .

log "Installing dependencies..."
install_dependencies

log "Setting up environment..."
setup_environment

log "Deploying smart contracts..."
deploy_smart_contracts

log "Starting application..."
start_application

log "Deployment completed successfully!"
