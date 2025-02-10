import pywayland
from pywayland.server import Display
from pywayland.protocol.wayland import WlCompositor, WlSeat, WlOutput
from pywayland.protocol.xdg_shell import XdgWmBase
from typing import Dict, Optional
import cairo
import os

class WaylandCompositor:
    def __init__(self):
        # First try to clean up any stale lock files
        lock_file = f"/run/user/{os.getuid()}/wayland-0.lock"
        try:
            os.remove(lock_file)
        except FileNotFoundError:
            pass
            
        self.display = Display()
        self.socket = self.display.add_socket()
        
        # Create global objects
        self.wl_compositor = WlCompositor()
        self.seat = WlSeat()
        self.xdg_shell = XdgWmBase()
        
        # Register globals directly on display
        self.display.global_create(self.wl_compositor, 4)
        self.display.global_create(self.seat, 7)
        self.display.global_create(self.xdg_shell, 1)
        
        # Initialize state
        self.surfaces: Dict[int, 'Surface'] = {}
        self.output = None
        
        # Set up listeners
        self.xdg_shell.dispatcher["create_positioner"] = self.handle_create_positioner
        self.xdg_shell.dispatcher["get_xdg_surface"] = self.handle_get_xdg_surface
        
    def run(self):
        print(f"Wayland compositor running on {self.socket}")
        try:
            while True:
                self.display.flush_clients()
                self.display.dispatch()
        except KeyboardInterrupt:
            print("\nShutting down compositor...")
        finally:
            self.display.destroy()
            
    def handle_create_positioner(self, client, resource, id):
        # Handle creation of surface positioners
        positioner = resource.create_positioner(id)
        
    def handle_get_xdg_surface(self, client, resource, id, surface):
        # Handle new XDG surfaces
        xdg_surface = resource.get_xdg_surface(id, surface)
        if xdg_surface:
            xdg_surface.dispatcher["get_toplevel"] = self.handle_get_toplevel
            
    def handle_get_toplevel(self, client, resource, id):
        # Handle toplevel windows
        toplevel = resource.get_toplevel(id)
        if toplevel:
            toplevel.dispatcher["set_title"] = self.handle_set_title
            
    def handle_set_title(self, client, resource, title):
        # Handle window title changes
        print(f"Window title changed: {title}")
        
    def damage_surface(self, surface_id: int):
        """Mark a surface as needing redraw"""
        if surface_id in self.surfaces:
            self.surfaces[surface_id].damaged = True
            
    def redraw(self):
        """Redraw all damaged surfaces"""
        for surface in self.surfaces.values():
            if surface.damaged:
                self.render_surface(surface)
                surface.damaged = False
                
    def render_surface(self, surface):
        """Render a single surface"""
        if surface.buffer:
            # Map the buffer and render with Cairo
            with surface.buffer.mmap() as pixels:
                surface_cairo = cairo.ImageSurface.create_for_data(
                    pixels,
                    cairo.FORMAT_ARGB32,
                    surface.width,
                    surface.height,
                    surface.stride
                )
                ctx = cairo.Context(surface_cairo)
                # Perform actual rendering here
                surface_cairo.flush()