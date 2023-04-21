from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4 as DISPLAY
from machine import Pin
import drawing_utils
from drawing_utils import BLACK,WHITE,GREEN,BLUE,RED,YELLOW,ORANGE,TAUPE

graphics = PicoGraphics(DISPLAY)

du = drawing_utils.ColorDither(graphics)

led_warn = Pin(6, Pin.OUT)

graphics.set_pen(WHITE)
graphics.rectangle(600, 0, 40, 200)
graphics.set_pen(BLACK)
graphics.rectangle(600, 200, 40, 200)

du.drawRectangleColors(0,0,100,100,[BLUE,WHITE])
du.drawRectangleColors(100,0,100,100,[BLUE])
du.drawRectangleColors(200,0,100,100,[BLUE,BLACK])

du.drawRectangleColors(0,100,100,100,[RED,WHITE])
du.drawRectangleColors(100,100,100,100,[RED])
du.drawRectangleColors(200,100,100,100,[RED,BLACK])

du.drawRectangleColors(0,200,100,100,[GREEN,WHITE])
du.drawRectangleColors(100,200,100,100,[GREEN])
du.drawRectangleColors(200,200,100,100,[GREEN,BLACK])

du.drawRectangleColors(0,300,100,100,[YELLOW,WHITE])
du.drawRectangleColors(100,300,100,100,[YELLOW])
du.drawRectangleColors(200,300,100,100,[YELLOW,BLACK])

du.drawRectangleColors(300,0,100,100,[ORANGE,WHITE])
du.drawRectangleColors(400,0,100,100,[ORANGE])
du.drawRectangleColors(500,0,100,100,[ORANGE,BLACK])

du.drawRectangleColors(300,100,100,100,[RED,BLUE])
du.drawRectangleColors(400,100,100,100,[RED,GREEN,BLACK])
du.drawRectangleColors(500,100,100,100,[GREEN,YELLOW])

du.drawRectangleColors(300,200,100,100,[BLUE,ORANGE])
du.drawRectangleColors(400,200,100,100,[GREEN,ORANGE])
du.drawRectangleColors(500,200,100,100,[GREEN,BLUE])
   
du.drawRectangleColors(300,300,100,100,[BLUE,GREEN,WHITE])
du.drawRectangleColors(400,300,100,100,[WHITE,BLUE,GREEN,WHITE])
du.drawRectangleColors(500,300,100,100,[RED,ORANGE])

du.drawRectangleColors(600,0,40,25,[BLACK])

du.drawRectangleDithering(600, 25,40,25,BLACK,WHITE,1)
du.drawRectangleDithering(600, 50,40,25,BLACK,WHITE,2)
du.drawRectangleDithering(600, 75,40,25,BLACK,WHITE,3)
du.drawRectangleDithering(600,100,40,25,BLACK,WHITE,4)
du.drawRectangleDithering(600,125,40,25,BLACK,WHITE,5)
du.drawRectangleDithering(600,150,40,25,BLACK,WHITE,6)
du.drawRectangleDithering(600,175,40,25,BLACK,WHITE,7)

du.drawRectangleColors(600,200,40,25,[BLACK,WHITE])

du.drawRectangleDithering(600,225,40,25,WHITE,BLACK,7)
du.drawRectangleDithering(600,250,40,25,WHITE,BLACK,6)
du.drawRectangleDithering(600,275,40,25,WHITE,BLACK,5)
du.drawRectangleDithering(600,300,40,25,WHITE,BLACK,4)
du.drawRectangleDithering(600,325,40,25,WHITE,BLACK,3)
du.drawRectangleDithering(600,350,40,25,WHITE,BLACK,2)
du.drawRectangleDithering(600,375,40,25,WHITE,BLACK,1)

led_warn.on()
graphics.update()
led_warn.off()

