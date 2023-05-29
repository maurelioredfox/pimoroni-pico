from machine import Pin
from pimoroni import ShiftRegister
import display_singleton
import gc
import json
import os
import jpegdec
import time

# set up and enable vsys hold so we don't go to sleep
HOLD_VSYS_EN_PIN = 2
hold_vsys_en_pin = Pin(HOLD_VSYS_EN_PIN, Pin.OUT)
hold_vsys_en_pin.value(True)

display = display_singleton.get_display()
WIDTH, HEIGHT = display.get_bounds()

#helper for colors
BLACK = 0
WHITE = 1
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6
TAUPE = 7

#pins
SR_CLOCK = 8
SR_LATCH = 9
SR_OUT = 10
sr = ShiftRegister(SR_CLOCK, SR_LATCH, SR_OUT)

#leds
number16_led = Pin(11, Pin.OUT)
number_8_led = Pin(12, Pin.OUT)
number_4_led = Pin(13, Pin.OUT)
number_2_led = Pin(14, Pin.OUT)
number_1_led = Pin(15, Pin.OUT)

#variables that are short
Colors = [{
    "Background": GREEN,
    "BackgroundBoxes": BLACK,
    "Text1": WHITE,
    "Text2": (77, 255, 77)
    },{
    "Background": (77, 34, 44),
    "BackgroundBoxes": (33, 11, 27),
    "Text1": (207, 171, 81),
    "Text2": (157, 101, 76)
    },{
    "Background": (80, 80, 112),
    "BackgroundBoxes": (234, 240, 216),
    "Text1": (65, 58, 66),
    "Text2": (31, 31, 41)
    }]

NAME = [{"name":"Pixylatte","size":2},{"name":"Aurunemaru","size":1.7}]
IMAGE = [{"file":"img/badge_pixy.jpg","name":0},{"file":"img/badge_auru.jpg","name":1},{"file":"img/badge_potat.jpg","name":0}]

gc.collect()

state = {"image":0, "border":1, "colors":0, "text":0, "new":True}
  
SKIP_DRAW = False
    
def file_exists(filename):
    try:
        return (os.stat(filename)[0] & 0x4000) == 0
    except OSError:
        return False
    
def save_state():
    global state
    with open("/badge_state.json", "w") as f:
        f.write(json.dumps(state))
        f.flush()

def load_state():
    global state
    data = json.loads(open("/badge_state.json", "r").read())
    if type(data) is dict:
        state = data
        
def show_number(number):
    number16_led.off()
    number_8_led.off()
    number_4_led.off()
    number_2_led.off()
    number_1_led.off()
    
    if(number& 1): number_1_led.on()
    if(number& 2): number_2_led.on()
    if(number& 4): number_4_led.on()
    if(number& 8): number_8_led.on()
    if(number&16): number16_led.on()

        
def safeSetPen(display, color):
    if type(color) is int:
        display.set_pen(color)
    else:
        display.set_pen(display.create_pen(color[0],color[1],color[2]))
    
def update():
    global SKIP_DRAW
    #if nothing changed from saved state, don't draw, duh
    SKIP_DRAW = True
    
    if file_exists("/badge_state.json"):
        load_state()
        
    result = sr.read()
    button_a = sr[7]
    button_b = sr[6]
    button_c = sr[5]
    button_d = sr[4]
    button_e = sr[3]
    
    if button_a or button_b or button_c or button_d or button_e:
        
        gc.collect()
        
        state["new"] = True
        
        if button_a: #picture
            button = 7
            maxvalue = 3
        #if button_b: #name
        #    button = 6
        #    maxvalue = 2
        if button_c: #border
            button = 5
            maxvalue = 2
        if button_d: #color
            button = 4
            maxvalue = 3
        if button_e: #text
            button = 3
            maxvalue = 3
        
        new_value = 1
        show_number(new_value)
        
        timeout = time.time() + 5 #5 seconds
        while time.time() < timeout:
            result = sr.read()
            if sr[button]:
                new_value = new_value + 1
            if new_value > maxvalue:
                new_value = 1
            
            show_number(new_value)
            time.sleep(0.2)
        show_number(0)
        
        gc.collect()
        
        if button is 7: #picture
            state["image"] = new_value - 1
        #if button is 6: #name
        #    state["name"] = new_value - 1
        if button is 5: #border
            state["border"] = new_value - 1
        if button is 4: #color
            state["colors"] = new_value - 1
        if button is 3: #text
            state["text"] = new_value - 1
    
    if state["new"]:
        SKIP_DRAW = False
        save_state()

def draw():
    #background
    safeSetPen(display,Colors[state["colors"]]["Background"])
    display.clear()
    
    #name
    safeSetPen(display,Colors[state["colors"]]["BackgroundBoxes"])
    display.rectangle(310,10,WIDTH-320,80)
    
    safeSetPen(display,Colors[state["colors"]]["Text1"])
    display.set_font("gothic")
    display.set_thickness(3)
    namenumber = IMAGE[state["image"]]["name"]
    display.text(NAME[namenumber]["name"],320,50,scale = NAME[namenumber]["size"])
    
    #picture
    gc.collect()
    
    jpeg = jpegdec.JPEG(display)
    jpeg.open_file(IMAGE[state["image"]]["file"])
    jpeg.decode(25,25,jpegdec.JPEG_SCALE_FULL) #plz 350 x 250
    del jpeg
    gc.collect()
    
    #border
    badgeborders = __import__("badgeborders")
    badgeborders.BORDERS[state["border"]](display)
    del badgeborders
    gc.collect()
    
    #text
            
    safeSetPen(display,Colors[state["colors"]]["BackgroundBoxes"])
    display.rectangle(310,110,320,280)
    
    badgetexts = __import__("badgetexts")
    badgetexts.texts[state["text"]](display,[Colors[state["colors"]]["Text1"],Colors[state["colors"]]["Text2"]])
    del badgetexts
    gc.collect()
    
    safeSetPen(display,WHITE)
    display.set_font("bitmap8")
    
    display.set_thickness(1)
    display.text("picture",80,392,scale = 1)
    #display.text("name",200,392,scale = 1)
    display.text("border",320,392,scale = 1)
    display.text("color",440,392,scale = 1)
    display.text("text",560,392,scale = 1)
    
    display.update()
    state["new"] = False
    save_state()
