from picographics import PicoGraphics, DISPLAY_TUFTY_2040

display = None

def get_display():
    global display
    if display == None:
        display = PicoGraphics(display=DISPLAY_TUFTY_2040)
    return display