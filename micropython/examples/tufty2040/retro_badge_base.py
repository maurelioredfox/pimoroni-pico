# A retro badge with photo and QR code.
# Copy your image to your Tufty alongside this example - it should be a 120 x 120 jpg.
from pimoroni import Button
import time
import jpegdec
import qrcode
import display_singleton
import random


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
    
    LIGHTEST_R = display.create_pen(255 - 208, 255 - 208, 255 - 88)
    LIGHT_R = display.create_pen(160, 168, 255 - 64)
    DARK_R = display.create_pen(255 - 112, 255 - 128, 255 - 40)
    DARKEST_R = display.create_pen(255 - 64, 255 - 80, 255 - 16)

    # Change your badge and QR details here!
    COMPANY_NAME = "sciurus cybernetics"
    NAME = "M. 'TuFTy'"
    BLURB1 = "RP2040 plus 320x240 TFT LCD"
    BLURB2 = "Nuts From Trees collector"
    BLURB3 = "Will work for peanuts"
    QR_TEXT = "pimoroni.com/tufty2040"
    IMAGE_NAME = "squirrel.jpg"

    TEXT_GLITCHES = ["%34@%$","$$F00D","______","F0█DDD","██████","aaaaaa"]
    CHAR_GLITCHES = ["�",'ã','█','Ø']

    # Some constants we'll use for drawing
    BORDER_SIZE = 4
    PADDING = 10
    COMPANY_HEIGHT = 40
    GLITCH_SCALE_X = 1
    GLITCH_SCALE_Y = 3
    GLITCH_SCALE_Y_BG = 7

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

        if(self.GLITCHY):
            self.display.set_pen(self.DARK_R)
            for _ in range(3):
                rect = (random.randint(1, (self.WIDTH - (self.BORDER_SIZE * 2)) // self.GLITCH_SCALE_X ), random.randint(1, (self.HEIGHT - (self.BORDER_SIZE * 2)) // self.GLITCH_SCALE_Y_BG))
                try:
                    origin = (random.randint(self.BORDER_SIZE, self.WIDTH - self.BORDER_SIZE - rect[0]), random.randint(self.BORDER_SIZE, self.HEIGHT - self.BORDER_SIZE - rect[1]))
                except:
                    print(f"rect {rect}, tried to make random({self.BORDER_SIZE},{self.WIDTH - self.BORDER_SIZE - rect[0]})")
                    print(f"rect {rect}, tried to make random({self.BORDER_SIZE},{self.HEIGHT - self.BORDER_SIZE - rect[1]})")
                self.display.rectangle(origin[0], origin[1], rect[0], rect[1])

        # draw company box
        self.display.set_pen(self.DARKEST)
        self.display.rectangle(self.BORDER_SIZE, self.BORDER_SIZE, self.WIDTH - (self.BORDER_SIZE * 2), self.COMPANY_HEIGHT)

        if(self.GLITCHY):
            self.display.set_pen(self.DARKEST_R)
            for _ in range(3):
                rect = (random.randint(1, (self.WIDTH - (self.BORDER_SIZE * 2)) // self.GLITCH_SCALE_X ), random.randint(1, self.COMPANY_HEIGHT // self.GLITCH_SCALE_Y))
                try:
                    origin = (random.randint(self.BORDER_SIZE, self.WIDTH - self.BORDER_SIZE - rect[0]), random.randint(self.BORDER_SIZE, self.BORDER_SIZE + self.COMPANY_HEIGHT - rect[1]))
                except:
                    print(f"rect {rect}, tried to make random({self.BORDER_SIZE},{self.WIDTH - self.BORDER_SIZE - rect[0]})")
                    print(f"rect {rect}, tried to make random({self.BORDER_SIZE},{self.COMPANY_HEIGHT - rect[1]})")
                self.display.rectangle(origin[0], origin[1], rect[0], rect[1])



        # draw company text
        self.display.set_pen(self.LIGHT)
        self.display.set_font("bitmap6")
        self.__draw_text(self.COMPANY_NAME, self.BORDER_SIZE + self.PADDING, self.BORDER_SIZE + self.PADDING, self.WIDTH, 3)

        # draw name text
        self.display.set_pen(self.LIGHTEST)
        self.display.set_font("bitmap8")
        self.__draw_text(self.NAME, self.BORDER_SIZE + self.PADDING, self.BORDER_SIZE + self.PADDING + self.COMPANY_HEIGHT, self.WIDTH, 5)

        # draws the bullet points
        self.display.set_pen(self.DARKEST)
        self.__draw_text("*", self.BORDER_SIZE + self.PADDING + 120 + self.PADDING, 105, 160, 2)
        self.__draw_text("*", self.BORDER_SIZE + self.PADDING + 120 + self.PADDING, 140, 160, 2)
        self.__draw_text("*", self.BORDER_SIZE + self.PADDING + 120 + self.PADDING, 175, 160, 2)

        # draws the blurb text (4 - 5 words on each line works best)
        self.display.set_pen(self.LIGHTEST)
        self.__draw_text(self.BLURB1, self.BORDER_SIZE + self.PADDING + 135 + self.PADDING, 105, 160, 2)
        self.__draw_text(self.BLURB2, self.BORDER_SIZE + self.PADDING + 135 + self.PADDING, 140, 160, 2)
        self.__draw_text(self.BLURB3, self.BORDER_SIZE + self.PADDING + 135 + self.PADDING, 175, 160, 2)

    def __draw_text(self, text, x, y, width, size):

        if(self.GLITCHY and random.randint(0,1) == 0):
            #replaces a random part of the text with a glitch
            actual_text = text
            glitch = random.choice(self.TEXT_GLITCHES)
            glitch_start = random.randint(0, len(actual_text) - len(glitch) if len(actual_text) - len(glitch) > 0 else 0)
            actual_text = actual_text[:glitch_start] + glitch + actual_text[glitch_start + len(glitch):]
            self.display.text(actual_text, x, y, width, size)
        else:
            self.display.text(text, x, y, width, size)

    def __draw_glitch_on_photo(self):

        print(f"{self.IMAGE_NAME[:-4]}_glitch.rgb332")

        #glitches with normal
        self.display.load_spritesheet(f"{self.IMAGE_NAME[:-4]}_glitch.rgb332")
        zeroX = self.BORDER_SIZE + self.PADDING
        zeroy = self.HEIGHT - (self.BORDER_SIZE + self.PADDING) - 120

        shifts = []
        for i in range(15):
            aumont = random.randint(1,6)
            shifts.append((random.randint(0,15 - aumont), random.randint(0,14), random.randint(-2,2), aumont))

        for move in shifts:

            for x in range(move[3]):
                self.display.sprite(move[0] + x, move[1], zeroX + (move[0] * 8) + (move[2] * 8) + (x * 8), zeroy + (move[1] * 8))

        #glitches with reversed color
        self.display.load_spritesheet(f"{self.IMAGE_NAME[:-4]}_glitch_2.rgb332")
        zeroX = self.BORDER_SIZE + self.PADDING
        zeroy = self.HEIGHT - (self.BORDER_SIZE + self.PADDING) - 120

        shifts = []
        for i in range(15):
            aumont = random.randint(1,6)
            shifts.append((random.randint(0,15 - aumont), random.randint(0,14), random.randint(-2,2), aumont))

        for move in shifts:

            for x in range(move[3]):
                self.display.sprite(move[0] + x, move[1], zeroX + (move[0] * 8) + (move[2] * 8) + (x * 8), zeroy + (move[1] * 8))


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
        
        if self.GLITCHY:
            self.__draw_glitch_on_photo()

    def __draw_GPU_glitch(self):
        # decides between nothing, squares, or chars
        random.seed((self.FRAME // 50) * 568773)
        glitch_type = random.randint(0,3)
        if glitch_type <= 1:
            return
        else:
            #draws squares:
            r,g,b = random.choice([0,255]), random.choice([0,255]), random.choice([0,255])
            self.display.set_pen(self.display.create_pen(r,g,b))
            #creates a random looking effect, with some repeating patterns
            square_size = (8)
            step_x = random.randint(2,4)
            step_y = random.randint(1,3)

            line_offset = random.randint(1,2)
            line_offset_threshold = random.randrange(3,7)

            chosen_char = random.choice(self.CHAR_GLITCHES)
            self.display.set_font("bitmap8")

            current_offset = 0
            for y in range(0, self.HEIGHT, square_size * step_y):
                if random.randint(0,10) > line_offset_threshold:
                    current_offset = current_offset - line_offset * square_size
                    
                for x in range(current_offset, self.WIDTH, square_size * step_x):
                    if glitch_type == 2:
                        self.display.rectangle(x,y,square_size,square_size)
                    else:
                        self.display.text(chosen_char, x, y, square_size, scale = 1)
                        self.display.text(chosen_char, x + 1,  y, square_size, scale = 1)
            



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
                #call last because it changes the random seed
                self.__draw_GPU_glitch()

    def set_colors(self, darkest, dark, light, lightest):
        self.DARKEST = self.display.create_pen(darkest[0], darkest[1], darkest[2])
        self.DARK = self.display.create_pen(dark[0], dark[1], dark[2])
        self.LIGHT = self.display.create_pen(light[0], light[1], light[2])
        self.LIGHTEST = self.display.create_pen(lightest[0], lightest[1], lightest[2])    
    
        self.LIGHTEST_R = self.display.create_pen(255  - lightest[0], 255 - lightest[1], 255 - lightest[2])
        self.LIGHT_R = self.display.create_pen(160 - light[0], 168 - light[1], 255 - light[2])
        self.DARK_R = self.display.create_pen(255 - dark[0], 255 - dark[1], 255 - dark[2])
        self.DARKEST_R = self.display.create_pen(255 - darkest[0], 255 - darkest[1], 255 - darkest[2])

    def main_loop(self):
        while True:
            if self.GLITCHY and self.FRAME % 10 == 0:
                self.CHANGED = True
                random.seed(self.FRAME // 10)
            self.__control()
            if self.CHANGED:
                self.CHANGED = False
                self.__draw()
                self.display.update()

            self.FRAME += 1
            self.FRAME %= 2000
            time.sleep(0.01)
