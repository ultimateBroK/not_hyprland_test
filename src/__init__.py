from .window_manager import WindowManager
from .compositor import Compositor
import xcffib
import signal
import sys

def main():
    compositor = Compositor()
    window_manager = WindowManager()
    
    def signal_handler(signum, frame):
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        while True:
            event = window_manager.conn.wait_for_event()
            if isinstance(event, xcffib.xproto.MapRequestEvent):
                window_manager.manage_window(event.window)
                compositor.damage_window(event.window)
            elif isinstance(event, xcffib.xproto.UnmapNotifyEvent):
                window_manager.unmanage_window(event.window)
            elif isinstance(event, xcffib.xproto.EnterNotifyEvent):
                window_manager.focus_window(event.event)
            
            compositor.redraw()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()