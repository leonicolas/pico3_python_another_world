"""SDL2 display and input backend using ctypes.

Provides a proper windowed display with true key-up/key-down detection
via SDL_GetKeyboardState. No C compilation needed.
"""

import hdmi
import time
import pcconsole; 
import pcgui

from aw.hal import DisplayHAL
from aw.consts import SCREEN_W, SCREEN_H

STRIDE = SCREEN_W // 2

class Pico3Display(DisplayHAL):

    def __init__(self):
        hdmi.deinit()
        hdmi.init(hdmi.RGB320)
        time.sleep(3) # let the monitor lock before drawing
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
            d = hdmi.fb()
            self._colour_lut = [d.colour(r, g, b) for r, g, b in palette]
 
    def present(self, framebuf_4bpp):
        d = hdmi.fb()
        pixel = d.pixel
        colours = self._colour_lut
        idx = 0
        for y in range(SCREEN_H):
            row = idx
            for x in range(0, SCREEN_W, 2):
                byte_val = framebuf_4bpp[row]
                pixel(x, y, colours[(byte_val >> 4) & 0x0F])
                pixel(x + 1, y, colours[byte_val & 0x0F])
                row += 1
            idx += STRIDE
        hdmi.copy("F", "N")

    def shutdown(self):
        # Cleanup Pico3 display resources
        print("Shutting down Pico3 display...")
        hdmi.write("N")
        hdmi.fill(0)
        self.gui.stop()
        pcconsole.console("both")
