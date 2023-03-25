import time
import machine
import display_singleton

display = display_singleton.get_display()
rtc = machine.RTC()
display.set_backlight(0.5)

# Tufty constants.
A = 7
B = 8
C = 15
UP = 22
DOWN = 6
LED = 25

WIDTH, HEIGHT = display.get_bounds()

# Buttons
button_a = machine.Pin(A, machine.Pin.IN)
button_b = machine.Pin(B, machine.Pin.IN)
button_c = machine.Pin(C, machine.Pin.IN)
button_up = machine.Pin(UP, machine.Pin.IN)
button_down = machine.Pin(DOWN, machine.Pin.IN)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

PINK = display.create_pen(214, 28, 78)
ORANGE_1 = display.create_pen(247, 126, 33)
ORANGE_2 = display.create_pen(250, 194, 19)

cursors = ["hour", "minute"]
set_clock = False
cursor = 0
last = 0

vbat_adc = machine.ADC(29)
vref_adc = machine.ADC(28)
vref_en = machine.Pin(27)
vref_en.init(machine.Pin.OUT)
vref_en.value(0)

def days_in_month(month, year):
    if month == 2 and ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
        return 29
    return (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[month - 1]


# Button handling function
def button(pin):
    global last, set_clock, cursor, year, month, day, hour, minute

    time.sleep(0.01)
    if not pin.value():
        return

    if button_a.value() and button_c.value():
        machine.reset()

    adjust = 0
    changed = False

    if pin == button_b:
        set_clock = not set_clock
        changed = True
        if not set_clock:
            rtc.datetime((year, month, day, 0, hour, minute, second, 0))

    if set_clock:
        if pin == button_c:
            cursor += 1
            cursor %= len(cursors)

        if pin == button_a:
            cursor -= 1
            cursor %= len(cursors)

        if pin == button_up:
            adjust = 1

        if pin == button_down:
            adjust = -1

        if cursors[cursor] == "hour":
            hour += adjust
            hour %= 24
        if cursors[cursor] == "minute":
            minute += adjust
            minute %= 60

    if set_clock or changed:
        draw_clock()


# Register the button handling function with the buttons
button_down.irq(trigger=machine.Pin.IRQ_RISING, handler=button)
button_up.irq(trigger=machine.Pin.IRQ_RISING, handler=button)
button_a.irq(trigger=machine.Pin.IRQ_RISING, handler=button)
button_b.irq(trigger=machine.Pin.IRQ_RISING, handler=button)
button_c.irq(trigger=machine.Pin.IRQ_RISING, handler=button)


def draw_clock():

    display.set_pen(WHITE)
    display.clear()

    hr = "{:02}".format(hour)
    min = "{:02}".format(minute)
    sec = "{:02}".format(second)

    hr_width = display.measure_text(hr, 1)
    hr_offset = 15

    minute_width = display.measure_text(min, 1)
    minute_offset = 15

    second_width = display.measure_text(sec, 1)
    second_offset = 5

    display.set_pen(PINK)
    display.rectangle(10, 10, (hour * 13), 60)
    display.set_pen(ORANGE_1)
    display.rectangle(10, 85, (minute * 5), 60)
    display.set_pen(ORANGE_2)
    display.rectangle(10, 160, (second * 5), 60)

    display.set_pen(WHITE)
    display.text(hr, (hour * 13) - hr_width - hr_offset, 45, 10, 3)
    display.text(min, (minute * 5) - minute_width - minute_offset, 120, 10, 3)
    display.text(sec, (second * 5) - second_width - second_offset, 202, 10, 2)

    display.set_pen(BLACK)

    if set_clock:

        if cursors[cursor] == "hour":
            display.line(5, 10, 5, 70)
        if cursors[cursor] == "minute":
            display.line(5, 85, 5, 145)

    display.update()

def get_voltage():
    vref_en.value(1)
    vdd = 1.24 * (65535 / vref_adc.read_u16())
    vbat = ((vbat_adc.read_u16() / 65535) * 3 * vdd ) 
    vref_en.value(0)
    return vbat

def register_bat():
    with open('batterylog.txt','a') as file:
        file.write('\n')
        file.write(('{};{}').format(last_time-zero,get_voltage()))
        print(('{};{}').format(last_time-zero,get_voltage()))
    

year, month, day, wd, hour, minute, second, _ = rtc.datetime()

last_second = second
zero = time.time()
last_time = zero

register_bat()

while True:
    if not set_clock:
        year, month, day, wd, hour, minute, second, _ = rtc.datetime()
        if second != last_second:
            draw_clock()
            last_second = second
    if last_time + 60 <= time.time():
        last_time = time.time()
        register_bat()
    time.sleep(0.01)
