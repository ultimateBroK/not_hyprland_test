#!/usr/bin/env python3
from .window_manager import WindowManager
from .compositor import WaylandCompositor
import os
import signal
import sys

def check_environment():
    if 'WAYLAND_DISPLAY' in os.environ:
        print("Error: Already running inside a Wayland session.")
        print("Please run from a TTY or X11 session instead.")
        sys.exit(1)
    
    if not os.environ.get('XDG_RUNTIME_DIR'):
        runtime_dir = f"/run/user/{os.getuid()}"
        if not os.path.exists(runtime_dir):
            print(f"Error: XDG_RUNTIME_DIR not set and {runtime_dir} does not exist")
            sys.exit(1)
        os.environ['XDG_RUNTIME_DIR'] = runtime_dir

def main():
    check_environment()
    
    compositor = WaylandCompositor()
    window_manager = WindowManager(compositor.display)
    
    def signal_handler(signum, frame):
        print("\nReceived signal to quit...")
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        print("Starting Wayland compositor...")
        compositor.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()