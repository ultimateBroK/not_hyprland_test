import xcffib
import xcffib.xproto
from typing import Dict, List, Optional

class WindowManager:
    def __init__(self):
        self.conn = xcffib.connect()
        self.screen = self.conn.get_setup().roots[0]
        self.windows: Dict[int, 'Window'] = {}
        self.focused_window: Optional[int] = None
        
        # Register for events
        mask = (
            xcffib.xproto.EventMask.SubstructureRedirect |
            xcffib.xproto.EventMask.SubstructureNotify |
            xcffib.xproto.EventMask.EnterWindow |
            xcffib.xproto.EventMask.LeaveWindow |
            xcffib.xproto.EventMask.ButtonPress
        )
        
        self.screen.root.change_attributes(event_mask=mask)
        self.conn.flush()
        
    def manage_window(self, window_id: int):
        """Add a window to be managed"""
        if window_id not in self.windows:
            self.windows[window_id] = window_id
            self.arrange_windows()
            
    def unmanage_window(self, window_id: int):
        """Stop managing a window"""
        if window_id in self.windows:
            del self.windows[window_id]
            self.arrange_windows()
            
    def arrange_windows(self):
        """Arrange windows in a tiling layout"""
        if not self.windows:
            return
            
        # Simple horizontal tiling layout
        window_width = self.screen.width_in_pixels // len(self.windows)
        x_position = 0
        
        for window_id in self.windows:
            self.conn.core.ConfigureWindow(
                window_id,
                xcffib.xproto.ConfigWindow.X | 
                xcffib.xproto.ConfigWindow.Y |
                xcffib.xproto.ConfigWindow.Width |
                xcffib.xproto.ConfigWindow.Height,
                [
                    x_position,
                    0,
                    window_width,
                    self.screen.height_in_pixels
                ]
            )
            x_position += window_width
            
        self.conn.flush()
        
    def focus_window(self, window_id: int):
        """Focus a specific window"""
        if window_id in self.windows:
            if self.focused_window:
                # Unfocus current window
                self.conn.core.ChangeSaveSet(
                    xcffib.xproto.SetMode.Delete,
                    self.focused_window
                )
            
            # Focus new window
            self.conn.core.ChangeSaveSet(
                xcffib.xproto.SetMode.Insert,
                window_id
            )
            self.focused_window = window_id
            self.conn.flush()