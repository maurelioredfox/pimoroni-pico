from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4 as DISPLAY
from machine import Pin

BLACK = 0
WHITE = 1
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6
TAUPE = 7

graphics = PicoGraphics(DISPLAY)

led_warn = Pin(6, Pin.OUT)

graphics.set_pen(WHITE)
graphics.rectangle(600, 0, 40, 200)
graphics.set_pen(BLACK)
graphics.rectangle(600, 200, 40, 200)

def testcolor(color,x,y):
    graphics.set_pen(color)
    graphics.rectangle(x * 100, y * 100, 100, 100) 
    
def test2shades(color1,color2,x1,y1):
    x0 = x1*100
    y0 = y1*100
    graphics.set_pen(color1)

    graphics.rectangle(x0, y0, 100, 100)

    graphics.set_pen(color2)

    for x in range(x0, x0+60):
        for y in range(y0, y0+100):
            if ((x + y) % 2 == 0):
                graphics.pixel(x, y)
                
    for x in range(x0 + 60, x0+100,10):
        for y in range(y0, y0+100,10):
            if ((x + y) % 20 == 0):
                graphics.rectangle(x, y,10,10)
    
def test3shades(color1,color2,color3,x1,y1):
    x0 = x1*100
    y0 = y1*100
    graphics.set_pen(color1)
    
    graphics.rectangle(x0, y0, 100, 100)
    
    graphics.set_pen(color2)

    for x in range(x0, x0+60):
        for y in range(y0, y0+100):
            if ((x + y) % 3 == 0):
                graphics.pixel(x, y)
                
    for x in range(x0 + 60, x0+100,10):
        for y in range(y0, y0+100,10):
            if ((x + y) % 30 == 0):
                graphics.rectangle(x, y,10,10)
           
    graphics.set_pen(color3)
    
    for x in range(x0, x0+60):
        for y in range(y0, y0+100):
            if ((x + y) % 3 == 1):
                graphics.pixel(x, y)
                
    for x in range(x0 + 60, x0+100,10):
        for y in range(y0, y0+100,10):
            if ((x + y) % 30 == 10):
                graphics.rectangle(x, y,10,10)
    
def test4shades(c1,c2,c3,c4,x1,y1):
    x0 = x1*100
    y0 = y1*100
    graphics.set_pen(c1)

    graphics.rectangle(x0, y0, 100, 100)

    graphics.set_pen(c2)

    for x in range(x0, x0+60):
        for y in range(y0, y0+100):
            if (y % 2 == 0 and x % 2 == 1):
                graphics.pixel(x, y)
          
    for x in range(x0 + 60, x0+100,10):
        for y in range(y0, y0+100,10):
            if (y % 20 == 0 and x % 20 == 10):
                graphics.rectangle(x, y,10,10)
                
    graphics.set_pen(c3)
    
    for x in range(x0, x0+60):
        for y in range(y0, y0+100):
            if (y % 2 == 1 and x % 2 == 0):
                graphics.pixel(x, y)
                
    for x in range(x0 + 60, x0+100,10):
        for y in range(y0, y0+100,10):
            if (y % 20 == 10 and x % 20 == 0):
                graphics.rectangle(x, y,10,10)
                
    graphics.set_pen(c4)
    
    for x in range(x0, x0+50):
        for y in range(y0, y0+100):
            if (y % 2 == 1 and x % 2 == 1):
                graphics.pixel(x, y)

    for x in range(x0 + 60, x0+100,10):
        for y in range(y0, y0+100,10):
            if (y % 20 == 10 and x % 20 == 10):
                graphics.rectangle(x, y,10,10)
                        
test2shades(BLUE,WHITE,0,0)
testcolor(BLUE,1,0)
test2shades(BLUE,BLACK,2,0)

test2shades(RED,WHITE,0,1)
testcolor(RED,1,1)
test2shades(RED,BLACK,2,1)

test2shades(GREEN,WHITE,0,2)
testcolor(GREEN,1,2)
test2shades(GREEN,BLACK,2,2)

test2shades(YELLOW,WHITE,0,3)
testcolor(YELLOW,1,3)
test2shades(YELLOW,BLACK,2,3)

test2shades(ORANGE,WHITE,3,0)
testcolor(ORANGE,4,0)
test2shades(ORANGE,BLACK,5,0)

test2shades(RED,BLUE,3,1)
        
#brown
test3shades(RED,GREEN,BLACK,4,1)

#lime

test2shades(GREEN,YELLOW,5,1)

test2shades(BLUE,ORANGE,3,2)

test2shades(GREEN,ORANGE,4,2)

test2shades(GREEN,BLUE,5,2)
            
#light bleen
test3shades(BLUE,GREEN,WHITE,3,3)
            
#lighter bleen
test4shades(WHITE,BLUE,GREEN,WHITE,4,3)
       
#pumpkin
test2shades(RED,ORANGE,5,3)

led_warn.on()
graphics.update()
led_warn.off()
