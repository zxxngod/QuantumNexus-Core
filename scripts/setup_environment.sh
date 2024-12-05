#!/bin/bash

# Set strict mode
set -euo pipefail

# Constants
REPO_URL="https://github.com/yourusername/QuantumNexus-Core.git"
DEPLOY_DIR="/opt/quantumnexus"
ENV_FILE=".env"
LOG_FILE="setup_environment.log"

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
    if command_exists apt-get; then
        sudo apt-get update
        sudo apt-get install -y \
            python3 \
            python3-pip \
            nodejs \
            npm \
            git \
            curl \
            wget \
            build-essential \
            libssl-dev \
            libffi-dev
    elif command_exists yum; then
        sudo yum install -y \
            python3 \
            python3-pip \
            nodejs \
            npm \
            git \
            curl \
            wget \
            gcc \
            gcc-c++ \
            openssl-devel \
            libffi-devel
    else
        log "Unsupported package manager. Please install dependencies manually."
        exit 1
    fi

    if command_exists pip; then
        pip install --upgrade pip
    else
        log "pip is not installed. Please install pip and try again."
        exit 1
    fi

    if command_exists npm; then
        npm install -g npm@latest
    else
        log "npm is not installed. Please install npm and try again."
        exit 1
    fi
}

# Function to set up environment variables
setup_environment_variables() {
    log "Setting up environment variables..."
    if [ -f "$ENV_FILE" ]; then
        export $(grep -v '^#' "$ENV_FILE" | xargs)
    else
        log "$ENV_FILE not found. Please create it with the necessary environment variables."
        exit 1
    fi
}

# Function to configure the system
configure_system() {
    log "Configuring the system..."
    # Assuming you have a script to configure the system
    if command_exists some_configuration_tool; then
        some_configuration_tool
    else
        log "Configuration tool is not installed. Please install it and try again."
        exit 1
    fi
}

# Main script execution
log "Starting environment setup..."

log "Cloning repository..."
git clone "$REPO_URL" .

log "Installing dependencies..."
install_dependencies

log "Setting up environment variables..."
setup_environment_variables

log "Configuring the system..."
configure_system

log "Environment setup completed successfully!"
