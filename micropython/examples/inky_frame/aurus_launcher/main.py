import gc
import time
from machine import reset
import inky_helper_custom as helper

# A short delay to give USB chance to initialise
time.sleep(0.5)

# Setup for the display.

# Turn any LEDs off that may still be on from last run.
helper.clear_button_leds()
helper.led_warn.off()

if helper.inky_frame.button_a.read() and helper.inky_frame.button_e.read():
    helper.update_state("menu")

if helper.inky_frame.button_d.read() and helper.inky_frame.button_e.read():
    helper.update_state("router")

if not helper.file_exists("state.json"):
    helper.update_state("menu")
# Loads the JSON and launches the app
helper.load_state()
helper.launch_app(helper.state['run'])

gc.collect()

# The main loop executes the update and draw function from the imported app,
# and then goes to sleep ZzzzZZz

while True:
    helper.led_warn.on()
    helper.app.update()
    if not helper.app.SKIP_DRAW:
        helper.app.draw()
    helper.led_warn.off()
    time.sleep(0.5)
    helper.sleep()
