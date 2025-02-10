#!/bin/bash

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run as root"
    exit 1
fi

# Function to clean up on exit
cleanup() {
    echo "Cleaning up..."
    sudo systemctl start gdm.service
    exit 0
}

# Set up cleanup on script exit
trap cleanup EXIT INT TERM

echo "This script will:"
echo "1. Stop the GNOME Display Manager"
echo "2. Switch to TTY2"
echo "3. Start the not-hyprland compositor"
echo ""
echo "Press Ctrl+C to exit and return to GNOME"
echo ""
read -p "Press Enter to continue..."

# Stop GDM
echo "Stopping GNOME Display Manager..."
sudo systemctl stop gdm.service

# Export required environment variables
export XDG_RUNTIME_DIR="/run/user/$UID"
export LIBSEAT_BACKEND=built-in

# Switch to TTY2 and run compositor
echo "Switching to TTY2..."
sudo chvt 2

# Wait a moment for TTY switch
sleep 1

# Run our compositor
not-hyprland