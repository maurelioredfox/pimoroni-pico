from pimoroni_i2c import PimoroniI2C
from pcf85063a import PCF85063A
from secrets import AP_SSID, AP_PASSWORD
from machine import Pin, PWM, Timer
import network
import math
import time
import inky_frame
import json
import os

# Pin setup for VSYS_HOLD needed to sleep and wake.
hold_vsys_en_pin = Pin(2, Pin.OUT)
led_warn = Pin(6, Pin.OUT)

# set up for the network LED
network_led_pwm = PWM(Pin(7))
network_led_pwm.freq(1000)
network_led_pwm.duty_u16(0)


# set the brightness of the network led
def network_led(brightness):
    brightness = max(0, min(100, brightness))  # clamp to range
    # gamma correct the brightness (gamma 2.8)
    value = int(pow(brightness / 100.0, 2.8) * 65535.0 + 0.5)
    network_led_pwm.duty_u16(value)


network_led_timer = Timer(-1)
network_led_pulse_speed_hz = 1


def network_led_callback(t):
    # updates the network led brightness based on a sinusoid seeded by the current time
    brightness = (math.sin(time.ticks_ms() * math.pi * 2 / (1000 / network_led_pulse_speed_hz)) * 40) + 60
    value = int(pow(brightness / 100.0, 2.8) * 65535.0 + 0.5)
    network_led_pwm.duty_u16(value)


# set the network led into pulsing mode
def pulse_network_led(speed_hz=1):
    global network_led_timer, network_led_pulse_speed_hz
    network_led_pulse_speed_hz = speed_hz
    network_led_timer.deinit()
    network_led_timer.init(period=50, mode=Timer.PERIODIC, callback=network_led_callback)


# turn off the network led and disable any pulsing animation that's running
def stop_network_led():
    global network_led_timer
    network_led_timer.deinit()
    network_led_pwm.duty_u16(0)
    
def access_point_start():
    
    pulse_network_led()
    ap = network.WLAN(network.AP_IF)
    ap.ifconfig(("192.168.4.1", "255.255.255.0", "192.168.4.1", "192.168.4.1"))
    ap.config(essid=AP_SSID, password=AP_PASSWORD) 
    ap.active(True)

    while ap.active == False:
      pass

    print("Access point active")
    print(ap.ifconfig())

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
