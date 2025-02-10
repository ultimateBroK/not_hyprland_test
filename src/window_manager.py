from pywayland.server import Display
from pywayland.protocol.xdg_shell import XdgWmBase, XdgToplevel
from typing import Dict, List, Optional
import os

class WindowManager:
    def __init__(self, display: Display):
        self.display = display
        self.windows: Dict[int, XdgToplevel] = {}
        self.focused_window: Optional[int] = None
        
        # Register XDG shell listeners
        self.xdg_shell = self.display.create_global(XdgWmBase)
        self.xdg_shell.dispatcher["get_xdg_surface"] = self.handle_xdg_surface
        
    def handle_xdg_surface(self, client, resource, id, surface):
        xdg_surface = resource.get_xdg_surface(id, surface)
        if xdg_surface:
            xdg_surface.dispatcher["get_toplevel"] = self.handle_toplevel
            self.manage_window(xdg_surface)
            
    def handle_toplevel(self, client, resource, id):
        toplevel = resource.get_toplevel(id)
        if toplevel:
            toplevel.dispatcher["set_title"] = self.handle_set_title
            toplevel.dispatcher["set_app_id"] = self.handle_set_app_id
            toplevel.dispatcher["destroy"] = self.handle_destroy
            
    def handle_set_title(self, client, resource, title):
        window_id = resource.get_user_data()
        if window_id in self.windows:
            self.windows[window_id].title = title
            
    def handle_set_app_id(self, client, resource, app_id):
        window_id = resource.get_user_data()
        if window_id in self.windows:
            self.windows[window_id].app_id = app_id
            
    def handle_destroy(self, client, resource):
        window_id = resource.get_user_data()
        self.unmanage_window(window_id)
        
    def manage_window(self, window):
        """Add a window to be managed"""
        window_id = id(window)
        self.windows[window_id] = window
        window.set_user_data(window_id)
        self.arrange_windows()
        
    def unmanage_window(self, window_id):
        """Stop managing a window"""
        if window_id in self.windows:
            del self.windows[window_id]
            if self.focused_window == window_id:
                self.focused_window = None
            self.arrange_windows()
            
    def arrange_windows(self):
        """Arrange windows in a tiling layout"""
        if not self.windows:
            return
            
        # Get output dimensions (assuming single output for now)
        output = self.display.globals[0]  # First output
        width = output.current_mode.width
        height = output.current_mode.height
        
        # Simple horizontal tiling layout
        window_width = width // len(self.windows)
        x_position = 0
        
        for window in self.windows.values():
            window.set_size(window_width, height)
            window.set_position(x_position, 0)
            x_position += window_width
            
        self.display.flush_clients()
        
    def focus_window(self, window_id: int):
        """Focus a specific window"""
        if window_id in self.windows:
            if self.focused_window != window_id:
                if self.focused_window:
                    # Unfocus current window
                    old_window = self.windows[self.focused_window]
                    old_window.set_activated(False)
                
                # Focus new window
                new_window = self.windows[window_id]
                new_window.set_activated(True)
                self.focused_window = window_id
                self.display.flush_clients()