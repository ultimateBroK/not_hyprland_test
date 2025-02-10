#!/usr/bin/env python3
import subprocess
import sys
import os

def check_package(package):
    try:
        if sys.platform.startswith('linux'):
            subprocess.check_call(['pkg-config', '--exists', package])
            print(f"✓ {package} is installed")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"✗ {package} is not installed")
        return False

def check_wayland_socket():
    wayland_display = os.environ.get('WAYLAND_DISPLAY')
    if wayland_display:
        print("✓ Wayland session detected")
        return True
    print("✗ No Wayland session detected")
    return False

def main():
    required_packages = [
        'wayland-server',
        'wayland-client',
        'wayland-protocols',
        'cairo'
    ]
    
    missing = False
    for package in required_packages:
        if not check_package(package):
            missing = True
            
    check_wayland_socket()
            
    if missing:
        print("\nPlease install missing dependencies:")
        print("For Debian/Ubuntu:")
        print("sudo apt-get install libwayland-dev wayland-protocols libcairo2-dev")
        print("\nFor Arch Linux:")
        print("sudo pacman -S wayland wayland-protocols cairo")
        sys.exit(1)
        
if __name__ == "__main__":
    main()