from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4 as DISPLAY
import jpegdec

display = PicoGraphics(DISPLAY)
display.set_pen(1)
display.rectangle(0,0,640,400)
display.set_pen(0)
display.rectangle(310,10,320,80)
    
display.set_pen(1)

display.set_font("gothic")
display.set_thickness(3)

display.text("Aurunemaru",320,50,scale = 1.7)

display.update()
