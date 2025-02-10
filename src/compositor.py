import xcffib
import xcffib.xproto
import cairocffi as cairo
from typing import Dict, Optional

class Compositor:
    def __init__(self):
        self.conn = xcffib.connect()
        self.screen = self.conn.get_setup().roots[0]
        self.windows: Dict[int, 'Window'] = {}
        
        # Create overlay window for compositing
        self.overlay = self.conn.generate_id()
        mask = xcffib.xproto.CW.BackPixel | xcffib.xproto.CW.EventMask
        values = [
            self.screen.black_pixel,
            xcffib.xproto.EventMask.Exposure |
            xcffib.xproto.EventMask.StructureNotify
        ]
        
        self.conn.core.CreateWindow(
            self.screen.root_depth,
            self.overlay,
            self.screen.root,
            0, 0, self.screen.width_in_pixels, self.screen.height_in_pixels,
            0,
            xcffib.xproto.WindowClass.InputOutput,
            self.screen.root_visual,
            mask,
            values
        )
        
        # Map the overlay window
        self.conn.core.MapWindow(self.overlay)
        self.conn.flush()
        
    def damage_window(self, window_id: int):
        """Mark a window as needing redraw"""
        if window_id in self.windows:
            self.windows[window_id].damaged = True
            
    def redraw(self):
        """Redraw all damaged windows"""
        surface = cairo.XCBSurface(
            self.conn,
            self.overlay,
            self.screen.root_visual,
            self.screen.width_in_pixels,
            self.screen.height_in_pixels
        )
        
        ctx = cairo.Context(surface)
        ctx.set_source_rgb(0, 0, 0)
        ctx.paint()
        
        for window in self.windows.values():
            if window.damaged:
                window.draw(ctx)
                window.damaged = False
                
        surface.flush()