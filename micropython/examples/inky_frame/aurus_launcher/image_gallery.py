from machine import Pin
import jpegdec
from pimoroni import ShiftRegister
import display_singleton
import inky_helper_custom as helper
import os
import json

# you can change your file names here
IMAGE = []
IMAGE.append("img/imageA.jpg")
IMAGE.append("img/imageB.jpg")
IMAGE.append("img/imageC.jpg")
IMAGE.append("img/imageD.jpg")
IMAGE.append("img/imageE.jpg")
IMAGE.append("img/camera.jpg")

current = 0

# set up the display
display = display_singleton.get_display()
WIDTH, HEIGHT = display.get_bounds()
SKIP_DRAW = True
state = None

# Inky Frame uses a shift register to read the buttons
SR_CLOCK = 8
SR_LATCH = 9
SR_OUT = 10
sr = ShiftRegister(SR_CLOCK, SR_LATCH, SR_OUT)

# set up the button LEDs
button_a_led = Pin(11, Pin.OUT)
button_b_led = Pin(12, Pin.OUT)
button_c_led = Pin(13, Pin.OUT)
button_d_led = Pin(14, Pin.OUT)
button_e_led = Pin(15, Pin.OUT)

# and the activity LED
activity_led = Pin(6, Pin.OUT)

# set up and enable vsys hold so we don't go to sleep
HOLD_VSYS_EN_PIN = 2
hold_vsys_en_pin = Pin(HOLD_VSYS_EN_PIN, Pin.OUT)
hold_vsys_en_pin.value(True)

def load_state():
    global state
    data = json.loads(open("/image_gallery_state.json", "r").read())
    if type(data) is dict:
        state = data
        
def clear_state():
    if helper.file_exists("/image_gallery_state.json"):
        os.remove("/image_gallery_state.json")
        
def update():
    global SKIP_DRAW
    global current
    global state
    
    if helper.file_exists("/image_gallery_state.json"):
        load_state()
    
    if state is not None:
        current = state['current']
        SKIP_DRAW = False
        clear_state()
        
    
    result = sr.read()
    button_a = sr[7]
    button_b = sr[6]
    button_c = sr[5]
    button_d = sr[4]
    button_e = sr[3]
    if button_a == 1:
        current = 0
        SKIP_DRAW = False
    elif button_b == 1:
        current = 1
        SKIP_DRAW = False
    elif button_c == 1:
        current = 2
        SKIP_DRAW = False
    elif button_d == 1:
        current = 3
        SKIP_DRAW = False
    elif button_e == 1:
        current = 4
        SKIP_DRAW = False

def draw():
    print("draw",IMAGE[current])
    j = jpegdec.JPEG(display)
    j.open_file(IMAGE[current])
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    display.update()