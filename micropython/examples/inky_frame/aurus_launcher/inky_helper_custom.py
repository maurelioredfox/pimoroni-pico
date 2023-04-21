from pimoroni_i2c import PimoroniI2C
from pcf85063a import PCF85063A
import math
from machine import Pin, PWM, Timer
import time
import inky_frame
import json
import os

# Pin setup for VSYS_HOLD needed to sleep and wake.
hold_vsys_en_pin = Pin(2, Pin.OUT)
led_warn = Pin(6, Pin.OUT)

def sleep():
    # this allows the device to go into sleep mode when on battery power.
    hold_vsys_en_pin.init(Pin.IN)

# Turns off the button LEDs
def clear_button_leds():
    inky_frame.button_a.led_off()
    inky_frame.button_b.led_off()
    inky_frame.button_c.led_off()
    inky_frame.button_d.led_off()
    inky_frame.button_e.led_off()

state = {"run": None}
app = None

def file_exists(filename):
    try:
        return (os.stat(filename)[0] & 0x4000) == 0
    except OSError:
        return False
    
def save_json(path,data):
    with open(path, "w") as f:
        f.write(json.dumps(data))
        f.flush()

def clear_state():
    if file_exists("state.json"):
        os.remove("state.json")

def save_state(data):
    with open("/state.json", "w") as f:
        f.write(json.dumps(data))
        f.flush()

def load_state():
    global state
    data = json.loads(open("/state.json", "r").read())
    if type(data) is dict:
        state = data

def update_state(running):
    global state
    state['run'] = running
    save_state(state)


def launch_app(app_name):
    global app
    app = __import__(app_name)
    print(app)
    update_state(app_name)
