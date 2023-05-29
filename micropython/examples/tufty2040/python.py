import display_singleton
from pimoroni import Button
import jpegdec
import time
import random


display = display_singleton.get_display()

j = jpegdec.JPEG(display)
j.open_file('pixysnack.jpg')

Width = 320
Height = 240

TEXT = 91
TEXT_SHADING = 66

gridX = 16
gridY = 12

moveTimer = 7
fruitTimer = 30

button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)

max_score = 0

def get_max_score():
    pass

class Snake():
    def __init__(self):
        self.snake = [(5,4),(6,4),(7,4),(8,4)]
        self.orientation = 'down'
        self.lastmove = 'left'
        self.ate = False
        
    def read_controls(self):
        if button_b.read() and self.lastmove is not 'right':
            self.orientation = 'left'
        if button_c.read() and self.lastmove is not 'left':
            self.orientation = 'right'
        if button_up.read() and self.lastmove is not 'down':
            self.orientation = 'up'
        if button_down.read() and self.lastmove is not 'up':
            self.orientation = 'down'
        
    def check_collisions(self,x,y) -> bool:
        for position in self.snake:
            if position[0] == x and position[1] == y:
                return True
        return False
    
    def check_self_collisions(self) -> bool:
        head = self.snake[0]
        if head[0] < 0 or head[1] < 0 or head[0] > 15 or head[1] > 11: return True
        for position in self.snake[1:]:
            if position[0] == head[0] and position[1] == head[1]:
                return True
        return False
        
    def move(self):
        position0 = self.snake[0][0]
        position1 = self.snake[0][1]
        if self.orientation == 'up':
            position1 -= 1
            self.lastmove = 'up'
        if self.orientation == 'down':
            position1 += 1
            self.lastmove = 'down'
        if self.orientation == 'left':
            position0 -= 1
            self.lastmove = 'left'
        if self.orientation == 'right':
            position0 += 1
            self.lastmove = 'right'
        self.snake.insert(0,(position0,position1))
        print(self.snake)
        if self.ate:
            self.ate = False
        else:
            self.snake.pop()
        
    def keeptail(self):
        self.ate = True
        
    def draw(self):
        display.set_pen(255)
        last = None
        for position in self.snake:
            display.rectangle(position[0]*20 + 3,position[1]*20 + 3,14,14)
            if last is not None:
                if   last[0] == position[0] - 1:
                    display.rectangle(    last[0]*20 + 17,    last[1]*20 +  3,6,14)
                elif last[0] == position[0] + 1:
                    display.rectangle(position[0]*20 + 17,position[1]*20 +  3,6,14)
                elif last[1] == position[1] - 1:
                    display.rectangle(    last[0]*20 +  3,    last[1]*20 + 17,14,6)
                elif last[1] == position[1] + 1:
                    display.rectangle(position[0]*20 +  3,position[1]*20 + 17,14,6)
            last = position
        

class Game:
    def __init__(self):
        get_max_score()
        self.state = "menu"
        self.timer = 0
        self.timer2 = 0
        
    def start(self):
        self.timerMove = 0
        self.timerSpawnPrey = 0
        self.snake = Snake()
        self.fruit = (random.randint(0,15),random.randint(0,11))
        self.state = "game"
        
    def read_controls(self):
        if self.state == "game":
            self.snake.read_controls()
            if button_a.read():
                self.state = "pause"
            
        if self.state == "menu":
            if button_a.read():
                self.start()
                
        if self.state == "pause":
            if button_a.read():
                self.state = "game"
        
    def has_fruit(self):
        return self.fruit is not None
        
    def spawn_fruit(self):
        self.fruit = (random.randint(0,15),random.randint(0,11))
  
    def update(self):
        if self.state == "game":
            self.timerMove += 1
            if not game.has_fruit():
                self.timerSpawnPrey += 1    
                if self.timerSpawnPrey >= fruitTimer:
                    game.spawn_fruit()
                    self.timerSpawnPrey = 0
            if self.timerMove >= moveTimer:
                self.snake.move()
                game.check_collisions()
                self.timerMove = 0
        
    def check_collisions(self):
        global max_score
        if self.snake.check_self_collisions():
            score = len(self.snake.snake) - 4
            max_score = score if score > max_score else max_score
            self.state = 'menu'
        if self.fruit is not None and self.snake.check_collisions(self.fruit[0],self.fruit[1]):
            self.snake.keeptail()
            self.fruit = None
        
    def draw(self):
        display.set_pen(0)
        display.clear()
        if self.fruit is not None:
            j.decode(self.fruit[0]*20,self.fruit[1]*20)
        self.snake.draw()
        
        if self.state == 'menu':
            display.set_pen(TEXT_SHADING)
            display.text("Snake",52,52, scale=6)
            display.set_pen(TEXT)
            display.text("Snake",50,50, scale=6)
            display.set_pen(TEXT_SHADING)
            display.text("Max Score: {}".format(max_score),52,102, scale=4)
            display.set_pen(TEXT)
            display.text("Max Score: {}".format(max_score),50,100, scale=4)
            display.set_pen(TEXT_SHADING)
            display.text("press A to start",52,152, scale=3)
            display.set_pen(TEXT)
            display.text("press A to start",50,150, scale=3)
        if self.state == 'pause':
            display.set_pen(TEXT_SHADING)
            display.text("Pause",102,102, scale=6)
            display.set_pen(TEXT)
            display.text("Pause",100,100, scale=6)
            
        display.update()
        
game = Game()
game.start()
display.set_font('bitmap8')

while True:
    game.read_controls()
    game.update()
    game.draw()
    time.sleep(0.01)
