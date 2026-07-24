"""SDL2 display and input backend using ctypes.

Provides a proper windowed display with true key-up/key-down detection
via SDL_GetKeyboardState. No C compilation needed.
"""

import hdmi
import pcconsole; 
import pcgui

from aw.hal import DisplayHAL
from aw.consts import SCREEN_W, SCREEN_H

STRIDE = SCREEN_W // 2

class Pico3Display(DisplayHAL):

    def __init__(self, scale=1):
        print("globals", globals())
        """
        Args:
            scale: integer window scale factor (2 = 640x480 window).
        """
        self.scale = scale
        hdmi.deinit()
        hdmi.init(hdmi.RGB640)
        #time.sleep(3) # let the monitor lock before drawing
        hdmi.create() # Create the offscreen framebuffer
        hdmi.fill(0) # clear to black — create() doesn't zero the buffer
        hdmi.write("F")
        pcconsole.console("serial")

        self.gui = pcgui.GUI()
        self.gui.start()

    def init(self, width, height):
        pass

    def update_palette(self, palette):
        if palette:
            self._palette = palette

    def present(self, framebuf_4bpp):
        d = hdmi.fb()
        scale = self.scale
        for y in range(SCREEN_H):
            for x in range(SCREEN_W):
                byte_index = (y * STRIDE) + (x // 2)
                byte_val = framebuf_4bpp[byte_index]
                if x % 2 == 0:
                    color_index = (byte_val >> 4) & 0x0F
                else:
                    color_index = byte_val & 0x0F
                r, g, b = self._palette[color_index]
                colour = d.colour(r, g, b)
                sx = x * scale
                sy = y * scale
                for dy in range(scale):
                    for dx in range(scale):
                        d.pixel(sx + dx, sy + dy, colour)
        hdmi.copy("F", "N")

    def shutdown(self):
        # Cleanup Pico3 display resources
        print("Shutting down Pico3 display...")
        hdmi.write("N")
        hdmi.fill(0)
        self.gui.stop()
        pcconsole.console("both")
