#!/bin/bash

# Set strict mode
set -euo pipefail

# Constants
LOG_FILE="system_health.log"
THRESHOLD_CPU=80
THRESHOLD_MEM=80
THRESHOLD_DISK=90
THRESHOLD_NET=1000  # in KB/s

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Function to check CPU usage
check_cpu_usage() {
    log "Checking CPU usage..."
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    if (( $(echo "$CPU_USAGE > $THRESHOLD_CPU" | bc -l) )); then
        log "WARNING: High CPU usage detected: ${CPU_USAGE}%"
    else
        log "CPU usage is normal: ${CPU_USAGE}%"
    fi
}

# Function to check memory usage
check_memory_usage() {
    log "Checking memory usage..."
    MEM_USAGE=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
    if (( $(echo "$MEM_USAGE > $THRESHOLD_MEM" | bc -l) )); then
        log "WARNING: High memory usage detected: ${MEM_USAGE}%"
    else
        log "Memory usage is normal: ${MEM_USAGE}%"
    fi
}

# Function to check disk usage
check_disk_usage() {
    log "Checking disk usage..."
    DISK_USAGE=$(df / | grep / | awk '{ print $5 }' | sed 's/%//g')
    if [ "$DISK_USAGE" -gt "$THRESHOLD_DISK" ]; then
        log "WARNING: High disk usage detected: ${DISK_USAGE}%"
    else
        log "Disk usage is normal: ${DISK_USAGE}%"
    fi
}

# Function to check network usage
check_network_usage() {
    log "Checking network usage..."
    RX_BYTES_BEFORE=$(cat /sys/class/net/eth0/statistics/rx_bytes)
    TX_BYTES_BEFORE=$(cat /sys/class/net/eth0/statistics/tx_bytes)
    sleep 1  # Wait for 1 second to measure the change
    RX_BYTES_AFTER=$(cat /sys/class/net/eth0/statistics/rx_bytes)
    TX_BYTES_AFTER=$(cat /sys/class/net/eth0/statistics/tx_bytes)

    RX_RATE=$(( (RX_BYTES_AFTER - RX_BYTES_BEFORE) / 1024 ))  # Convert to KB
    TX_RATE=$(( (TX_BYTES_AFTER - TX_BYTES_BEFORE) / 1024 ))  # Convert to KB

    if [ "$RX_RATE" -gt "$THRESHOLD_NET" ] || [ "$TX_RATE" -gt "$THRESHOLD_NET" ]; then
        log "WARNING: High network usage detected: RX ${RX_RATE} KB/s, TX ${TX_RATE} KB/s"
    else
        log "Network usage is normal: RX ${RX_RATE} KB/s, TX ${TX_RATE} KB/s"
    fi
}

# Main script execution
log "Starting system health monitoring..."

# Create or clear the log file
: > "$LOG_FILE"

# Perform health checks
check_cpu_usage
check_memory_usage
check_disk_usage
check_network_usage

log "System health monitoring completed!"
