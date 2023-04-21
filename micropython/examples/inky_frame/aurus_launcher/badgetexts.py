import gc
import jpegdec

#your area is from 310,110 to 630,390
def safeSetPen(display, color):
    if type(color) is int:
        display.set_pen(color)
    else:
        display.set_pen(display.create_pen(color[0],color[1],color[2]))

#default stuff
def texts0(display,colors):
    safeSetPen(display,colors[1])
    display.set_font("bitmap8")
    display.set_thickness(2)
    display.text("Sylveon (Pixy)",335,130,wordwrap=285,scale = 4)
    display.text("DeerFox (Auru)",335,180,wordwrap=285,scale = 4)
    display.text("Turns coffee into IndexErrors",335,230,wordwrap=285,scale = 3)
    display.text("Yep, that's an Inky frame 4.0, Raspberry pi pico powered, 640x400 7 color e-Paper display",335,300,wordwrap=215,scale = 2)
    
    #brazil flag
    display.set_pen(2) #green
    display.rectangle(560,345,50,35)
    display.set_pen(5) #yellow
    display.polygon([(585,345),(610,363),(585,380),(560,363)])
    display.set_pen(3) #blue
    display.circle(585,363,10)
    display.set_pen(1) #white
    display.line(575,363,595,363,2)

#nutrition facts
def texts1(display,colors):
    safeSetPen(display,colors[0])
    display.set_thickness(2)
    display.line(311,111,628,111)
    display.line(311,388,628,388)
    display.line(311,111,311,388)
    display.line(628,111,628,388)
    
    display.set_thickness(1)
    display.line(315,207,625,207)
    display.line(315,223,625,223)
    display.line(315,239,625,239)
    display.line(315,255,625,255)
    display.line(315,271,625,271)
    display.line(315,287,625,287)
    display.line(315,303,625,303)
    display.line(315,319,625,319)
    display.line(315,335,625,335)
    display.line(315,351,625,351)
    display.line(315,367,625,367)
    
    display.rectangle(315,180,310,10)
    
    display.set_font("bitmap8")
    display.text("Nutrition Facts",325,125,scale = 4)
    
    safeSetPen(display,colors[1])
    display.set_font("serif")
    display.set_thickness(2)
    display.text("Serving size:",325,170,scale = 0.5)
    display.text("one 80kg mass",440,170,scale = 0.5)
    
    display.text("Aumont Per Serving",325,200,scale = 0.5)
    display.text("Calories 110,000     % Daily Value*",325,216,scale = 0.5)
    display.text("Total Fat 20Kg              30,769%",325,232,scale = 0.5)
    display.text("Cholesterol 100g           333,333%",325,248,scale = 0.5)
    display.text("Sodium 120g                 5,000%",325,264,scale = 0.5)
    display.text("Carbohidrates 1.2Kg           400%",325,280,scale = 0.5)
    display.text("Protein 12.6Kg             181,333%",325,296,scale = 0.5)
    display.text("Calcium  1.0Kg             90,909%",325,312,scale = 0.5)
    display.text("Iron 4.2g                    30,000%",325,328,scale = 0.5)
    display.text("Vitamin A 730mg           73,000%",325,344,scale = 0.5)
    display.text("Vitamin B12 5mg            2,500%",325,360,scale = 0.5)
    display.text("Vitamin C 1.6g               2,666%",325,376,scale = 0.5)

#moves
def texts2(display,colors):
    
    safeSetPen(display,colors[0])
    display.set_font("bitmap8")
    display.text("Current Moves",335,130,wordwrap=285,scale = 4)
    safeSetPen(display,colors[1])
    display.set_thickness(2)
    display.text("Charm",360,180,wordwrap=285,scale = 3)
    display.text("Tera Blast",360,220,wordwrap=285,scale = 3)
    display.text("Moonblast",360,260,wordwrap=285,scale = 3)
    display.text("Draining Kiss",360,300,wordwrap=285,scale = 3)
    
    #it's RAMming time
    gc.collect()
    
    jpeg = jpegdec.JPEG(display)
    jpeg.open_file("badgetext_fairy.jpg")
    jpeg.decode(320,173,jpegdec.JPEG_SCALE_FULL)
    jpeg.decode(320,253,jpegdec.JPEG_SCALE_FULL)
    jpeg.decode(320,293,jpegdec.JPEG_SCALE_FULL)
    
    gc.collect()
    
    safeSetPen(display,[150,150,150])
    display.rectangle(320,213,30,30)
    safeSetPen(display,[255,255,255])
    display.circle(335,228,12)
    safeSetPen(display,[150,150,150])
    display.circle(335,228,9)
    
    safeSetPen(display,colors[1])
    
    display.text("Lv. 70",335,350,wordwrap=285,scale = 4)
    
    safeSetPen(display,[234,93,234])
    display.rectangle(510,330,50,50)
    jpeg.decode(520,340,jpegdec.JPEG_SCALE_FULL)
    
    safeSetPen(display,[255,0,0])
    display.triangle(595,325,620,369,570,369)
    display.triangle(595,385,620,341,570,341)
    display.polygon([(595,330),(616,343),(616,367),(595,380),(574,367),(574,343)])
    
    jpeg.open_file("badgetext_fire.jpg")
    jpeg.decode(580,340,jpegdec.JPEG_SCALE_FULL)

texts = []
texts.append(texts0)
texts.append(texts1)
texts.append(texts2)