import display_singleton

display = display_singleton.get_display()

display.set_pen(display.create_pen(255, 255, 255))
display.clear()

width,height = display.get_bounds()

display.set_pen(display.create_pen(0,128, 0))
display.rectangle(20,20,width-40,height-40)

display.set_pen(display.create_pen(255,255,0))
display.polygon([(20,height//2),(width//2,height-20),(width-20,height//2),(width//2,20)])

display.set_pen(display.create_pen(0,0,128))
display.circle(width//2,height//2,60)

#read a part of the screen
param = None

display.get_framebuffer(param)

display.update()
