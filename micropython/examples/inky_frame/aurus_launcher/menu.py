import gc
import time
from machine import reset
import inky_helper_custom as helper
import display_singleton

display = display_singleton.get_display()

# Setup for the display.
WIDTH, HEIGHT = display.get_bounds()
display.set_font("bitmap8")

def set_pixy():
    state = {"name": 0, "image":0, "border":1,"colors":0, "text":0, "new":True}
    helper.save_json("/badge_state.json",state)

def set_auru():
    state = {"name": 1, "image":1, "border":1,"colors":0, "text":0, "new":True}
    helper.save_json("/badge_state.json",state)
    
def reload_last():
    pass

SKIP_DRAW = False

def draw():
    global SKIP_DRAW
    SKIP_DRAW = True

    # Draws the menu
    display.set_pen(1)
    display.clear()

    display.set_pen(5)
    display.rectangle(0, 0, WIDTH, 50)
    display.set_pen(0)
    display.text("Launcher", 245, 10, WIDTH, 4)

    display.set_pen(4)
    display.rectangle(30, 60, WIDTH - 100, 50)
    display.set_pen(1)
    display.text("A. BADGE PIXY", 35, 75, 600, 3)


    display.set_pen(6)
    display.rectangle(30, 120, WIDTH - 130, 50)
    display.set_pen(1)
    display.text("B. BADGE AURU", 35, 135, 600, 3)


    display.set_pen(5)
    display.rectangle(30, 180, WIDTH - 160, 50)
    display.set_pen(1)
    display.text("C. IMAGE GALLERY", 35, 195, 600, 3)

    display.set_pen(0)
    display.text("Hold A + E, then press Reset, to return to the Launcher", 65, 370, 600, 2)

    helper.led_warn.on()
    display.update()
    helper.led_warn.off()

def update():
    if helper.inky_frame.button_a.read():
        helper.inky_frame.button_a.led_on()
        set_pixy()
        helper.update_state("badge")
        time.sleep(0.5)
        reset()
    if helper.inky_frame.button_b.read():
        helper.inky_frame.button_b.led_on()
        set_auru()
        helper.update_state("badge")
        time.sleep(0.5)
        reset()
    if helper.inky_frame.button_c.read():
        helper.inky_frame.button_c.led_on()
        helper.update_state("image_gallery")
        time.sleep(0.5)
        reset()