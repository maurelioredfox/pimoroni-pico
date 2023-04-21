from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4 as DISPLAY

display = None
display = PicoGraphics(DISPLAY)
def get_display():
    global display
    if display == None:
        display = PicoGraphics(display=DISPLAY_INKY_FRAME_4)
    return display