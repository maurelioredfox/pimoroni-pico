# A retro badge with photo and QR code.
# Copy your image to your Tufty alongside this example - it should be a 120 x 120 jpg.
from pimoroni import Button
import time
import jpegdec
import qrcode
import display_singleton


class Badge:

    display = display_singleton.get_display()
    button_c = Button(9, invert=False)
    button_b = Button(8, invert=False)

    WIDTH, HEIGHT = display.get_bounds()

    # Uncomment one of these four colour palettes - find more at lospec.com !
    # Nostalgia colour palette by WildLeoKnight - https://lospec.com/palette-list/nostalgia
    LIGHTEST = display.create_pen(208, 208, 88)
    LIGHT = display.create_pen(160, 168, 64)
    DARK = display.create_pen(112, 128, 40)
    DARKEST = display.create_pen(64, 80, 16)

    # Change your badge and QR details here!
    COMPANY_NAME = "sciurus cybernetics"
    NAME = "M. 'TuFTy'"
    BLURB1 = "RP2040 plus 320x240 TFT LCD"
    BLURB2 = "Nuts From Trees collector"
    BLURB3 = "Will work for peanuts"
    QR_TEXT = "pimoroni.com/tufty2040"
    IMAGE_NAME = "squirrel.jpg"

    # Some constants we'll use for drawing
    BORDER_SIZE = 4
    PADDING = 10
    COMPANY_HEIGHT = 40

    GLITCHY = False
    MODE = "photo"
    CHANGED = True
    FRAME = 0

    def __draw_badge(self):
        # draw border
        self.display.set_pen(self.LIGHTEST)
        self.display.clear()

        # draw background
        self.display.set_pen(self.DARK)
        self.display.rectangle(self.BORDER_SIZE, self.BORDER_SIZE, self.WIDTH - (self.BORDER_SIZE * 2), self.HEIGHT - (self.BORDER_SIZE * 2))

        # draw company box
        self.display.set_pen(self.DARKEST)
        self.display.rectangle(self.BORDER_SIZE, self.BORDER_SIZE, self.WIDTH - (self.BORDER_SIZE * 2), self.COMPANY_HEIGHT)

        # draw company text
        self.display.set_pen(self.LIGHT)
        self.display.set_font("bitmap6")
        self.display.text(self.COMPANY_NAME, self.BORDER_SIZE + self.PADDING, self.BORDER_SIZE + self.PADDING, self.WIDTH, 3)

        # draw name text
        self.display.set_pen(self.LIGHTEST)
        self.display.set_font("bitmap8")
        self.display.text(self.NAME, self.BORDER_SIZE + self.PADDING, self.BORDER_SIZE + self.PADDING + self.COMPANY_HEIGHT, self.WIDTH, 5)

        # draws the bullet points
        self.display.set_pen(self.DARKEST)
        self.display.text("*", self.BORDER_SIZE + self.PADDING + 120 + self.PADDING, 105, 160, 2)
        self.display.text("*", self.BORDER_SIZE + self.PADDING + 120 + self.PADDING, 140, 160, 2)
        self.display.text("*", self.BORDER_SIZE + self.PADDING + 120 + self.PADDING, 175, 160, 2)

        # draws the blurb text (4 - 5 words on each line works best)
        self.display.set_pen(self.LIGHTEST)
        self.display.text(self.BLURB1, self.BORDER_SIZE + self.PADDING + 135 + self.PADDING, 105, 160, 2)
        self.display.text(self.BLURB2, self.BORDER_SIZE + self.PADDING + 135 + self.PADDING, 140, 160, 2)
        self.display.text(self.BLURB3, self.BORDER_SIZE + self.PADDING + 135 + self.PADDING, 175, 160, 2)


    def __show_photo(self):
        j = jpegdec.JPEG(self.display)

        # Open the JPEG file
        j.open_file(self.IMAGE_NAME)

        # Draws a box around the image
        self.display.set_pen(self.DARKEST)
        self.display.rectangle(self.PADDING, self.HEIGHT - ((self.BORDER_SIZE * 2) + self.PADDING) - 120, 120 + (self.BORDER_SIZE * 2), 120 + (self.BORDER_SIZE * 2))

        # Decode the JPEG
        j.decode(self.BORDER_SIZE + self.PADDING, self.HEIGHT - (self.BORDER_SIZE + self.PADDING) - 120)

        # Draw QR button label
        self.display.set_pen(self.LIGHTEST)
        self.display.text("QR", 240, 215, 160, 2)


    def __measure_qr_code(self, size, code):
        w, _ = code.get_size()
        module_size = int(size / w)
        return module_size * w, module_size


    def __draw_qr_code(self, ox, oy, size, code):
        size, module_size = self.__measure_qr_code(size, code)
        self.display.set_pen(self.LIGHTEST)
        self.display.rectangle(ox, oy, size, size)
        self.display.set_pen(self.DARKEST)
        for x in range(size):
            for y in range(size):
                if code.get_module(x, y):
                    self.display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)

    def __draw_glitch(self):
        fixed_seed = self.FRAME // 10


    def __show_qr(self):
        self.display.set_pen(self.DARK)
        self.display.clear()

        code = qrcode.QRCode()
        code.set_text(self.QR_TEXT)

        size, _ = self.__measure_qr_code(self.HEIGHT, code)
        left = int((self.WIDTH // 2) - (size // 2))
        top = int((self.HEIGHT // 2) - (size // 2))
        self.__draw_qr_code(left, top, self.HEIGHT, code)

    def __control(self):

        if self.button_b.is_pressed:
            print("Button B pressed")
            self.GLITCHY = not self.GLITCHY

        if self.button_c.is_pressed:
            print("Button C pressed")
            self.CHANGED = True
            if self.MODE == "photo":
                self.MODE = "qr"
            else:
                self.MODE = "photo"

    def __draw(self):
        if self.MODE == "qr":
            self.__show_qr()
        else:
            self.__draw_badge()
            self.__show_photo()
            if self.GLITCHY:
                self.__draw_glitch()
        self.display.update()

    def set_colors(self, darkest, dark, light, lightest):
        self.DARKEST = self.display.create_pen(darkest[0], darkest[1], darkest[2])
        self.DARK = self.display.create_pen(dark[0], dark[1], dark[2])
        self.LIGHT = self.display.create_pen(light[0], light[1], light[2])
        self.LIGHTEST = self.display.create_pen(lightest[0], lightest[1], lightest[2])

    def main_loop(self):
        while True:
            if self.GLITCHY and self.FRAME % 10 == 0:
                self.CHANGED = True

            self.__control()
            if self.CHANGED:
                self.CHANGED = False
                self.__draw()
                self.display.update()

            self.FRAME += 1
            self.FRAME %= 300
            time.sleep(0.01)
