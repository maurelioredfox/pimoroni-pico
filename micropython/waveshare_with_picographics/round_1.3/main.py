import time
import math
from pimoroni_bus import SPIBus
from picographics import PicoGraphics, DISPLAY_ROUND_LCD_240X240, PEN_RGB565
from machine import Pin, SPI
import jpegdec


def write_data(buf):
    cs(1)
    dc(1)
    cs(0)
    spi.write(bytearray([buf]))
    cs(1)
    
def write_cmd(cmd):
    cs(1)
    dc(0)
    cs(0)
    spi.write(bytearray([cmd]))
    cs(1)
    
def init():
    rst(1)
    time.sleep(0.01)
    rst(0)
    time.sleep(0.01)
    rst(1)
    time.sleep(0.05)
    
    write_cmd(0xEF)
    write_cmd(0xEB)
    write_data(0x14) 
    
    write_cmd(0xFE) 
    write_cmd(0xEF) 

    write_cmd(0xEB)
    write_data(0x14) 

    write_cmd(0x84)
    write_data(0x40) 

    write_cmd(0x85)
    write_data(0xFF) 

    write_cmd(0x86)
    write_data(0xFF) 

    write_cmd(0x87)
    write_data(0xFF)

    write_cmd(0x88)
    write_data(0x0A)

    write_cmd(0x89)
    write_data(0x21) 

    write_cmd(0x8A)
    write_data(0x00) 

    write_cmd(0x8B)
    write_data(0x80) 

    write_cmd(0x8C)
    write_data(0x01) 

    write_cmd(0x8D)
    write_data(0x01) 

    write_cmd(0x8E)
    write_data(0xFF) 

    write_cmd(0x8F)
    write_data(0xFF) 


    write_cmd(0xB6)
    write_data(0x00)
    write_data(0x20)

    write_cmd(0x36)
    write_data(0x90)

    write_cmd(0x3A)
    write_data(0x05) 


    write_cmd(0x90)
    write_data(0x08)
    write_data(0x08)
    write_data(0x08)
    write_data(0x08) 

    write_cmd(0xBD)
    write_data(0x06)
    
    write_cmd(0xBC)
    write_data(0x00)

    write_cmd(0xFF)
    write_data(0x60)
    write_data(0x01)
    write_data(0x04)

    write_cmd(0xC3)
    write_data(0x13)
    write_cmd(0xC4)
    write_data(0x13)

    write_cmd(0xC9)
    write_data(0x22)

    write_cmd(0xBE)
    write_data(0x11) 

    write_cmd(0xE1)
    write_data(0x10)
    write_data(0x0E)

    write_cmd(0xDF)
    write_data(0x21)
    write_data(0x0c)
    write_data(0x02)

    write_cmd(0xF0)   
    write_data(0x45)
    write_data(0x09)
    write_data(0x08)
    write_data(0x08)
    write_data(0x26)
    write_data(0x2A)

    write_cmd(0xF1)    
    write_data(0x43)
    write_data(0x70)
    write_data(0x72)
    write_data(0x36)
    write_data(0x37)  
    write_data(0x6F)


    write_cmd(0xF2)   
    write_data(0x45)
    write_data(0x09)
    write_data(0x08)
    write_data(0x08)
    write_data(0x26)
    write_data(0x2A)

    write_cmd(0xF3)   
    write_data(0x43)
    write_data(0x70)
    write_data(0x72)
    write_data(0x36)
    write_data(0x37) 
    write_data(0x6F)

    write_cmd(0xED)
    write_data(0x1B) 
    write_data(0x0B) 

    write_cmd(0xAE)
    write_data(0x77)
    
    write_cmd(0xCD)
    write_data(0x63)


    write_cmd(0x70)
    write_data(0x07)
    write_data(0x07)
    write_data(0x04)
    write_data(0x0E) 
    write_data(0x0F) 
    write_data(0x09)
    write_data(0x07)
    write_data(0x08)
    write_data(0x03)

    write_cmd(0xE8)
    write_data(0x34)

    write_cmd(0x62)
    write_data(0x18)
    write_data(0x0D)
    write_data(0x71)
    write_data(0xED)
    write_data(0x70) 
    write_data(0x70)
    write_data(0x18)
    write_data(0x0F)
    write_data(0x71)
    write_data(0xEF)
    write_data(0x70) 
    write_data(0x70)

    write_cmd(0x63)
    write_data(0x18)
    write_data(0x11)
    write_data(0x71)
    write_data(0xF1)
    write_data(0x70) 
    write_data(0x70)
    write_data(0x18)
    write_data(0x13)
    write_data(0x71)
    write_data(0xF3)
    write_data(0x70) 
    write_data(0x70)

    write_cmd(0x64)
    write_data(0x28)
    write_data(0x29)
    write_data(0xF1)
    write_data(0x01)
    write_data(0xF1)
    write_data(0x00)
    write_data(0x07)

    write_cmd(0x66)
    write_data(0x3C)
    write_data(0x00)
    write_data(0xCD)
    write_data(0x67)
    write_data(0x45)
    write_data(0x45)
    write_data(0x10)
    write_data(0x00)
    write_data(0x00)
    write_data(0x00)

    write_cmd(0x67)
    write_data(0x00)
    write_data(0x3C)
    write_data(0x00)
    write_data(0x00)
    write_data(0x00)
    write_data(0x01)
    write_data(0x54)
    write_data(0x10)
    write_data(0x32)
    write_data(0x98)

    write_cmd(0x74)
    write_data(0x10)
    write_data(0x85)
    write_data(0x80)
    write_data(0x00) 
    write_data(0x00) 
    write_data(0x4E)
    write_data(0x00)
    
    write_cmd(0x98)
    write_data(0x3e)
    write_data(0x07)

    write_cmd(0x35)
    write_cmd(0x21)

    write_cmd(0x11)
    time.sleep(0.12)
    write_cmd(0x29)
    time.sleep(0.02)
    
    write_cmd(0x21)

    write_cmd(0x11)

    write_cmd(0x29)

    write_cmd(0x36)
    write_data(0x98)
    
def prepare_show():
    write_cmd(0x2A)
    write_data(0x00)
    write_data(0x00)
    write_data(0x00)
    write_data(0xef)

    write_cmd(0x2B)
    write_data(0x00)
    write_data(0x00)
    write_data(0x00)
    write_data(0xEF)

    write_cmd(0x2C)

def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)  # XXX assume int() truncates!
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q

rst = Pin(12,Pin.OUT)
spi = SPI(1,100_000_000,polarity=0, phase=0,sck=Pin(10),mosi=Pin(11),miso=None)
dc = Pin(8,Pin.OUT)
cs = Pin(9,Pin.OUT)

spibus = SPIBus(dc=8, cs=9, sck=10, mosi=11, bl=25)

display = PicoGraphics(display=DISPLAY_ROUND_LCD_240X240, bus=spibus, pen_type=PEN_RGB565)
display.set_backlight(1.0)

init()

WIDTH, HEIGHT = display.get_bounds()
RADIUS = WIDTH // 2

BLACK = display.create_pen(0, 0, 0)

t = 0

while True:
    display.set_pen(BLACK)
    display.clear()

    angle = t % (math.pi * 2)

    prev_x = RADIUS
    prev_y = RADIUS

    steps = 30.0
    angle_step = 0.5
    
    j = jpegdec.JPEG(display)
    j.open_file("auru-240.jpg")
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)
    
    display.set_font('bitmap8')
    display.set_pen(display.create_pen(255,0,0))
    display.text("RED", 50, 50, scale=2)
    display.set_pen(display.create_pen(0,255,0))
    display.text("GREEN", 100, 50, scale=2)
    display.set_pen(display.create_pen(0,0,255))
    display.text("BLUE", 150, 50, scale=2)
    

    for step in range(int(steps)):
        angle += angle_step

        distance = RADIUS / steps * step
        distance += step * 0.2

        r, g, b = [int(c * 255) for c in hsv_to_rgb((t / 10.0) + distance / 120.0, 1.0, 1.0)]

        x = RADIUS + int(distance * math.cos(angle))
        y = RADIUS + int(distance * math.sin(angle))

        radius = ((math.sin(t + angle) + 1) / 2.0) * 10
        dot_colour = display.create_pen(r, g, b)
        display.set_pen(dot_colour)
        display.circle(int(x), int(y), int(radius))

        prev_x = x
        prev_y = y
        
    
    prepare_show()
    display.update()
    time.sleep(0.01)
    t += 0.01

