import display_singleton

display = display_singleton.get_display()

display.set_font('bitmap6')

for i in range(0,16):
    for j in range (0,16):
        display.set_pen(i*16 + j)
        display.text('{}'.format(i*16 + j),i*20,j*12)
        
display.update()