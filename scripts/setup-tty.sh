#!/bin/bash

# Colors for better visibility in TTY
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo_step() {
    echo -e "${GREEN}[+]${NC} $1"
}

echo_error() {
    echo -e "${RED}[!]${NC} $1"
}

# Check if running in TTY
if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    echo_error "Please run this script from a TTY (Ctrl+Alt+F2)"
    exit 1
fi

# Step 1: Install system dependencies
echo_step "Step 1: Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    sudo apt-get update
    sudo apt-get install -y python3-pip python3-venv git \
        libwayland-dev wayland-protocols libcairo2-dev \
        pkg-config
elif command -v pacman &> /dev/null; then
    # Arch Linux
    sudo pacman -S --noconfirm python python-pip git \
        wayland wayland-protocols cairo pkg-config
else
    echo_error "Unsupported distribution. Please install dependencies manually."
    exit 1
fi

# Step 2: Create and activate virtual environment
echo_step "Step 2: Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 3: Install the package
echo_step "Step 3: Installing not-hyprland..."
pip install -e .

# Step 4: Set required environment variables
echo_step "Step 4: Setting up environment variables..."
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export LIBSEAT_BACKEND=built-in

# Step 5: Run dependency check
echo_step "Step 5: Checking dependencies..."
python3 scripts/check_dependencies.py

if [ $? -eq 0 ]; then
    echo_step "All dependencies are satisfied!"
    echo_step "You can now run 'not-hyprland' to start the compositor"
    echo_step "Press Ctrl+C to exit the compositor"
else
    echo_error "Please install missing dependencies and try again"
    exit 1
fi