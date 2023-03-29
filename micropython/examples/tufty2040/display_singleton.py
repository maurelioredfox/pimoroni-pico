from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332

display = None

def get_display():
    global display
    if display == None:
        display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332, rotate=180)
    return display