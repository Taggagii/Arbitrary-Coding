import time
import pyautogui as p
from pynput import keyboard
import math

running = True
def on_press(key):
    if (keyboard.Key.scroll_lock == key): # soft kill
        global running
        running = False
        
    if (keyboard.Key.print_screen == key): # hard kill
        while True:
            p.FAILSAFE = True
            # moving mouse to corner of screen causes pyautogui built in failsafe to be triggered
            p.moveTo(0, 0) 


listener = keyboard.Listener(on_press = on_press)
listener.start()

yorg = 800
xorg = -1600

p.moveTo(xorg, yorg);
inaccuracy = 10
scaler = 50
x = 0
xmax = 500
while (running and x < xmax):
    p.dragTo(xorg + x, yorg + scaler * math.sin(x/scaler))
    x += inaccuracy

listener.stop()
