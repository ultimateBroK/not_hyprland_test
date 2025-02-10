#!/usr/bin/env python3
import subprocess
import sys

def check_package(package):
    try:
        if sys.platform.startswith('linux'):
            # Try using pkg-config to check for X11 libraries
            subprocess.check_call(['pkg-config', '--exists', package])
            print(f"✓ {package} is installed")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"✗ {package} is not installed")
        return False

def main():
    required_packages = [
        'xcb',
        'cairo',
        'xorg-server',
        'x11'
    ]
    
    missing = False
    for package in required_packages:
        if not check_package(package):
            missing = True
            
    if missing:
        print("\nPlease install missing dependencies:")
        print("For Debian/Ubuntu:")
        print("sudo apt-get install libx11-dev libcairo2-dev libxcb-composite0-dev xorg")
        print("\nFor Arch Linux:")
        print("sudo pacman -S libx11 cairo xcb-util xorg-server")
        sys.exit(1)
        
if __name__ == "__main__":
    main()