import display_singleton
from pimoroni import Button
import time
import random

display = display_singleton.get_display()

button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)

# MENU VARIABLES
t = time.ticks_ms() / 1000.0

selected_item = 2
scroll_position = 2
target_scroll_position = 2
    
grid_size = 40
    
selected_pen = display.create_pen(255, 255, 255)
unselected_pen = display.create_pen(80, 80, 100)
background_pen = display.create_pen(50, 50, 70)
shadow_pen = display.create_pen(0, 0, 0)
d4_pen = display.create_pen(25, 163, 66)
d6_pen = display.create_pen(29, 192, 211)
d8_pen = display.create_pen(151, 59, 227)
d8_pen2 = display.create_pen(88, 31, 160)
d8_pen3 = display.create_pen(33, 2, 87)
d10_pen = display.create_pen(227, 43, 150)
d10_pen2 = display.create_pen(176, 23, 108)
d10_pen3 = display.create_pen(112, 1, 63)
d12_pen = display.create_pen(219, 60, 65)
d12_pen2 = display.create_pen(219, 35, 42)
d12_pen3 = display.create_pen(180, 20, 20)
d20_pen = display.create_pen(243, 128, 0)
d20_pen2 = display.create_pen(243, 103, 0)
d20_pen3 = display.create_pen(243, 70, 0)
d20_pen4 = display.create_pen(188, 41, 0)
d100_pen = display.create_pen(134, 140, 152)
    
#show fixed list, or menu?
dicesold = [(0,"8d4",[4,4,4,4,4,4,4,4]),
         (1,"4d6",[6,6,6,6]),
         (2,"4d8",[8,8,8,8]),
         (3,"8d6",[6,6,6,6,6,6,6,6]),
         (4,"12D6",[6,6,6,6,6,6,6,6,6,6,6,6]),
         (5,"12D8",[8,8,8,8,8,8,8,8,8,8,8,8]),
         (6,"D12",[12]),
         (7,"D20",[20]),
         (8,"12D20",[20,20,20,20,20,20,20,20,20,20,20,20]),
         (9,"D100",[100]),
         (9,"test",[4,6,8,10,12,20])]

dices = [(0,"D4",[4]),
         (1,"D6",[6]),
         (2,"D8",[8]),
         (3,"D10",[10]),
         (4,"D12",[12]),
         (5,"D20",[20]),
         (6,"D100",[100])]

state = "menu"
selected_dice = None
just_rolled = False
results = None
aumont = 1

def hsv_to_rgb(h: float, s: float, v: float) -> tuple[float, float, float]:
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    v = int(v * 255)
    t = int(t * 255)
    p = int(p * 255)
    q = int(q * 255)
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
       
def input_menu():
    global target_scroll_position
    global selected_item
    global scroll_position
    global state
    global selected_dice
    global aumont
    
    if button_up.read():
        target_scroll_position -= 1
        target_scroll_position = target_scroll_position if target_scroll_position >= 0 else len(dices) - 1

    if button_down.read():
        target_scroll_position += 1
        target_scroll_position = target_scroll_position if target_scroll_position < len(dices) else 0
        
    if button_a.read():
        aumont -= 1
        if aumont < 1: aumont = 1
            
    if button_c.read():
        aumont += 1
        if aumont > 12: aumont = 12
            
    if button_b.read():
        while button_a.is_pressed:
            time.sleep(0.01)

        selected_dice = []
        for i in range(0,aumont):
            selected_dice.append(dices[selected_item][2][0])
        draw_dice()
        state = "dice"
    
def draw_menu():
    global target_scroll_position
    global selected_item
    global scroll_position
    global aumont
    
    #background
    display.set_pen(background_pen)
    display.clear()
    for y in range(0, 240 // grid_size):
        for x in range(0, 320 // grid_size):
            h = x + y + int(t * 5)
            h = h / 50.0
            r, g, b = hsv_to_rgb(h, 0.5, 1)

            display.set_pen(display.create_pen(r, g, b))
            display.rectangle(x * grid_size, y * grid_size, grid_size, grid_size)
            
    #menu itens
    scroll_position += (target_scroll_position - scroll_position) / 5
    
    selected_item = round(target_scroll_position)

    for application in dices:
        
        distance = application[0] - scroll_position
        text_size = 1.2 if selected_item == application[0] else 1

        # center text horixontally
        title_width = display.measure_text(application[1], text_size)
        text_x = int(160 - title_width / 2)
        row_height = text_size * 5 + 20

        # center list items vertically
        text_y = int(120 + distance * row_height - (row_height / 2))

        # draw the text, selected item brightest and with shadow
        if selected_item == application[0]:
            display.set_pen(shadow_pen)
            display.text(str(aumont)+application[1], text_x + 1, text_y + 1, -1, text_size)

        text_pen = selected_pen if selected_item == application[0] else unselected_pen
        display.set_pen(text_pen)
        display.text(str(aumont)+application[1], text_x, text_y, -1, text_size) 
        
def menu():
    draw_menu()
    input_menu()
    
def roll(selected_dice) -> []:
    results = []
    for dice in selected_dice:
        results.append(random.randint(1,dice))
    return results
    
def input_dice():
    global results
    global just_rolled
    global selected_dice
    global state
    
    if button_b.read():
        results = roll(selected_dice)
        just_rolled = True
    if button_c.read():
        results = None
        state = "menu"

def draw_each_dice(x: int, y: int,type: int):
    if   type is 4:
        display.set_pen(d4_pen)
        display.polygon([(x+40,y),(x+5,y+60),(x+75,y+60)])
    elif type is 6:
        display.set_pen(d6_pen)
        display.rectangle(x+10,y+10,60,60)
    elif type is 8:
        display.set_pen(d8_pen3)
        display.polygon([(x+40,y+75),(x+10,y+62),(x+70,y+62)])
        display.set_pen(d8_pen2)
        display.polygon([(x+40,y+5),(x+10,y+62),(x+10,y+25)])
        display.polygon([(x+40,y+5),(x+70,y+25),(x+70,y+62)])
        display.set_pen(d8_pen)
        display.polygon([(x+40,y+5),(x+10,y+62),(x+70,y+62)])
    elif type is 10:
        top = (x+40,y+8)
        left = (x+18,y+50)
        right = (x+58,y+50)
        down = (x+40,y+60)
        
        display.set_pen(d10_pen3)
        display.polygon([down,left,(x+10,y+50),(x+40,y+72)])
        display.polygon([down,right,(x+70,y+50),(x+40,y+72)])
        display.set_pen(d10_pen2)
        display.polygon([top,left,(x+10,y+50),(x+10,y+35)])
        display.polygon([top,right,(x+70,y+50),(x+70,y+35)])
        display.set_pen(d10_pen)
        display.polygon([top,left,down,right])
        
    elif type is 12:
        top = (x+40,y+13)
        leftup = (x+17,y+30)
        rightup = (x+63,y+30)
        leftdown = (x+25,y+55)
        rightdown = (x+55,y+55)
        display.set_pen(d12_pen3)
        display.polygon([leftdown,rightdown,(x+63,y+65),(x+40,y+75),(x+17,y+65)])
        display.polygon([top,leftup,(x+7,y+25),(x+20,y+10),(x+40,y+3)])
        display.polygon([top,(x+40,y+3),(x+60,y+10),(x+73,y+25),rightup])
        display.set_pen(d12_pen2)
        display.polygon([leftup,leftdown,(x+17,y+65),(x+7,y+48),(x+7,y+25)])
        display.polygon([rightup,rightdown,(x+63,y+65),(x+73,y+48),(x+73,y+25)])
        display.set_pen(d12_pen)
        display.polygon([top,leftup,leftdown,rightdown,rightup])
        
    elif type is 20:
        maintop = (x+40,y+20)
        mainleft = (x+20,y+55)
        mainright = (x+60,y+55)
        secbottom = (x+40,y+75)
        secleft = (x+10,y+26)
        secrigth = (x+70,y+26)
        display.set_pen(d20_pen4)
        display.polygon([(x+70,y+55),secbottom,mainright])
        display.polygon([(x+10,y+55),mainleft,secbottom])
        display.set_pen(d20_pen3)
        display.polygon([secbottom,mainleft,mainright])
        display.polygon([(x+70,y+55),secrigth,mainright])
        display.polygon([(x+10,y+55),mainleft,secleft])
        display.polygon([maintop,secrigth,(x+40,y+5)])
        display.polygon([maintop,(x+40,y+5),secleft])
        display.set_pen(d20_pen2)
        display.polygon([maintop,secrigth,mainright])
        display.polygon([maintop,mainleft,secleft])
        display.set_pen(d20_pen)
        display.polygon([maintop,mainleft,mainright])
    elif type is 100:
        pass
    
def draw_dice():
    global selected_dice
    
    rows = 3 if(len(selected_dice) > 8) else 2 if(len(selected_dice) > 4) else 1
    display.set_pen(255)
    display.clear()
    
    counter = 0
    for y in range(0,rows):
        h = int((240/rows) * ( y + 1/2))
        for x in range(0,4):
            draw_each_dice(80*x,h-40,selected_dice[counter])
            counter += 1
            if counter == len(selected_dice): return

def draw_numbers():
    global results
    
    rows = 3 if(len(selected_dice) > 8) else 2 if(len(selected_dice) > 4) else 1
    display.set_pen(255)
    #loop to look random
    counter = 0
    for y in range(0,rows):
        h = int((240/rows) * ( y + 1/2))
        for x in range(0,4):
            w = int(80*(x + 1/2))
            text_size = display.measure_text(str(results[counter]), 1.2)
            display.text(str(results[counter]),w-int(text_size/2),h,scale=1.2)
            counter += 1
            if counter == len(results): return
    
def dice():
    global results
    global just_rolled
    input_dice()
    if just_rolled:
        for i in range(0,30):
            results = roll(selected_dice)
            draw_dice()
            draw_numbers()
            display.update()
            time.sleep(0.03)
        display.set_pen(0)
        summ = 0
        for value in results:
            summ += value
        display.set_font('bitmap6')
        display.text("sum: {}".format(summ),7,7,scale=2)
        display.set_font('sans')
        just_rolled = False
    

display.set_font('sans')
display.set_thickness(4)
        
while True:
    t = time.ticks_ms() / 1000.0
    if state == "menu":
        menu()
    if state == "dice":
        dice()
    display.update()
    time.sleep(0.01)
