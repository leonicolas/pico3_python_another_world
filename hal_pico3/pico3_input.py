"""Pico3 input backend using keyboard state polling.

Uses SDL_GetKeyboardState for true held-key detection — no terminal
repeat hacks needed. Supports simultaneous key presses.
"""

from keyboard import keydown, UP, DOWN, LEFT, RIGHT, ENTER, ESC
from aw.hal import InputHAL, InputState

# Scancodes
SC_ESCAPE = 41
SC_SPACE = 44
SC_RETURN = 40
SC_UP = 82
SC_DOWN = 81
SC_LEFT = 80
SC_RIGHT = 79
SC_W = 26
SC_A = 4
SC_S = 22
SC_D = 7
SC_P = 19
SC_N = 17
SC_Q = 20

class Pico3Input(InputHAL):
    def __init__(self):
        pass

    def poll(self):
        state = InputState()

        state.left = False
        state.right = False
        state.up = False
        state.down = False
        state.action = False
        
        for index in range(keydown()):
            key = keydown(index + 1)
            if key == UP or key == ord("w") or key == ord("W"):
                state.up = True
            elif key == DOWN or key == ord("s") or key == ord("S"):
                state.down = True
            elif key == LEFT or key == ord("a") or key == ord("A"):
                state.left = True
            elif key == RIGHT or key == ord("d") or key == ord("D"):
                state.right = True
            elif key == ord(" ") or key == ENTER:    
                state.action = True
            elif key == ESC or key == ord("q") or key == ord("Q"):
                state.quit = True

        # state.quit = "quit" in self._oneshot
        # state.pause = "pause" in self._oneshot
        # state.step = "step" in self._oneshot
        # self._oneshot.clear()

        return state

    def shutdown(self):
        pass
