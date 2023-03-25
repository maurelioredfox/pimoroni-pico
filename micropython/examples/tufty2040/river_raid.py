import time
import random
from pimoroni import Button
import display_singleton

display = display_singleton.get_display()
WIDTH, HEIGHT = display.get_bounds() # 320 , 240

BULLET_SPEED = 10
PLAYER_SPEED = 6
MAP_SPEED = 2

YELLOW = display.create_pen(255, 255, 0)

TERRAINS = [0b00000011,0b00001111,0b00111111,0b11000011,0b00011111,0b00000111,0b11000011]

BRIDGE_TERRAIN = 0b00111111
PRE_BRIDGE_TERRAIN = 0b00000111

spritesheet = bytearray(128 * 128)
open("player.rgb332", "rb").readinto(spritesheet)

# Buttons
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False, hold_time = 0)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)

display.set_backlight(0.7)
display.set_pen(255)
display.clear()



class Player():
    def __init__(self):
        #set starting state here
        self.x = 150
        self.y = 210
        self.height = 19
        self.width = 28
        self.fuel = 1000
        self.sprite = 2
        self.isAlive = True
        
    def move(self,x,y):
        if self.x + x > 0 - self.width and self.x + x < WIDTH - self.width:
            self.x += x
    
    def draw(self):
        display.set_spritesheet(spritesheet)
        display.sprite(0 + self.sprite,0,self.x     ,self.y -  5,2,255)
        display.sprite(0 + self.sprite,1,self.x     ,self.y + 11,2,255)
        display.sprite(1 + self.sprite,0,self.x + 16,self.y -  5,2,255)
        display.sprite(1 + self.sprite,1,self.x + 16,self.y + 11,2,255)
        display.set_pen(YELLOW)
        display.text("Fuel", 260, 200, scale=2)
        display.rectangle(260,220,round(50*(self.fuel/1000)),10)
        display.rectangle(260,215,50, 2)
        
class Shot():
    def __init__(self, x):
        self.x = x + 14
        self.y = 200
        self.width = 4
        self.height = 7
    
    def update(self):
        self.y -= BULLET_SPEED
    
    def draw(self):
        display.set_pen(YELLOW)
        display.line(self.x,self.y,self.x,self.y+7,4)

class Target():
    def __init__(self,x,y,width,height,limitX,limitY):
        self.isAlive = True
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.limitX = limitX
        self.limitY = limitY
        self.is_Ally = False
        
    def should_delete(self):
        return (not self.isAlive) or self.y > 240
    
    def update(self):
        self.y += MAP_SPEED
    
    def draw(self):
        raise "not implemented"

class Bridge(Target):
    def __init__(self,y):
        self.road1 = display.create_pen(140,140,140)
        self.road2 = display.create_pen(180,180,180)
        self.road3 = display.create_pen(255,255,0)
        super().__init__(120,y,80,28,0,0)
        
        
    def should_delete(self):
        return self.y > 240
    
    def draw(self):
        if self.isAlive:
           for tileX in range(0,5):
               for tileY in range(0,2):
                    display.sprite(6+tileX,tileY,self.x + 16*tileX,self.y + 1 + 16*tileY,2,255)
        display.set_pen(self.road1)
        display.rectangle(0,self.y,120,32)
        display.rectangle(200,self.y,120,32)
        display.set_pen(self.road2)
        display.rectangle(0,self.y + 4,120,24)
        display.rectangle(200,self.y + 4,120,24)
        display.set_pen(self.road3)
        display.rectangle(0,self.y + 14,120,4)
        display.rectangle(200,self.y + 14,120,4)
        
        
class Fuel(Target):
    def __init__(self,x,y):
        super().__init__(x,y,24,56,0,0)
        self.is_Ally = True
        
    def draw(self):
        display.sprite(0,2,self.x -  4,self.y     ,2,0)
        display.sprite(0,3,self.x -  4,self.y + 16,2,0)
        display.sprite(0,4,self.x -  4,self.y + 32,2,0)
        display.sprite(0,5,self.x -  4,self.y + 48,2,0)
        display.sprite(1,2,self.x + 12,self.y     ,2,0)
        display.sprite(1,3,self.x + 12,self.y + 16,2,0)
        display.sprite(1,4,self.x + 12,self.y + 32,2,0)
        display.sprite(1,5,self.x + 12,self.y + 48,2,0)

class Game():
    
    def __init__(self):
        self.player = Player()
        self.state = "playing"
        self.SKY_PEN = display.create_pen(72, 180, 224)
        self.TERRAIN_PEN = display.create_pen(16, 140, 16)
        self.bullets = []
        self.terrain = []
        self.targets = []
        self.terrain.append(TERRAINS[2])
        self.terrain.append(TERRAINS[1])
        self.terrain.append(TERRAINS[0])
        self.terrain.append(TERRAINS[2])
        self.terrain.append(TERRAINS[2])
        self.terrain_offset = 0
        self.terrain_number = 5
        self.new_terrain = False
        self.spawn_bridge = False
    
    def check_collision(self,a,b):
        return a.x + a.width >= b.x and a.x <= b.x + b.width and a.y + a.height >= b.y and a.y <= b.y + b.height
    
    def check_collision_terrain(self):
        for y,terrain in enumerate(self.terrain):
            coord_y = 200 - (y*120) + self.terrain_offset
            if(coord_y < 225 and coord_y > 110):
                for x in range(0,8):
                    if(terrain & (1 << x)):
                        if self.player.x + self.player.width >      20*x  and self.player.x < 20*x + 20:
                            self.player.isAlive = False
                        if self.player.x + self.player.width > 300-(20*x) and self.player.x < 320-(20*x):
                            self.player.isAlive = False
                        
    #read movements
    def process_input(self):
        if button_b.raw():
            self.player.move(PLAYER_SPEED, 0)
            self.player.sprite = 4
        elif button_a.raw():
            self.player.move(-PLAYER_SPEED, 0)
            self.player.sprite = 0
        else:
            self.player.sprite = 2
        if button_c.read() and len(self.bullets) == 0:
            self.bullets.append(Shot(self.player.x))
           
    def update_terrain(self):
        self.terrain_offset += MAP_SPEED
        if(self.terrain_offset >= 120):
            self.new_terrain = True
            self.terrain_offset = 0
            self.terrain.pop(0)
            if self.terrain_number % 8 == 0: #it's bridge time
                self.spawn_bridge = True
                self.terrain.append(BRIDGE_TERRAIN)
                intersection = ~self.terrain[-2] & ~self.terrain[-1] & 0xff
                match = False
                for i in range(0,7):
                    if intersection & (1 << i) and intersection & (1 << (i + 1)):
                        match = True
                        break
                if not match:
                    self.terrain[-2] = PRE_BRIDGE_TERRAIN
            elif(random.randint(0,1)):
                self.terrain.append(self.terrain[-1])
            else:
                while True:
                    newterrain = TERRAINS[random.randint(0,6)]
                    intersection = ~newterrain & ~self.terrain[-1] & 0xff
                    found = False
                    for i in range(0,7):
                        if intersection & (1 << i) and intersection & (1 << (i + 1)):
                            self.terrain.append(newterrain)
                            found = True
                            break
                    if found: break
            self.terrain_number += 1
        pass
    
    def spawn_targets(self):
        if self.spawn_bridge:
            self.spawn_bridge = False
            bridge = Bridge(-240)
            self.targets.append(bridge)
        elif self.new_terrain:
            self.new_terrain = False
            #get the bonduaries of current tile
            terrain = self.terrain[-2]
            max_x = 320
            for i in range(0,6):
                if terrain & (1 << i):
                    max_x = 320 - (i+1) * 20
            min_x = 320 - max_x
            bifurcated = (terrain & 0b11000000) > 0
            #decide for fuel
            if random.randint(0,2) == 2:
                if bifurcated:
                    side = random.randint(0,1)
                    if side:
                        min_x = 200
                    else:
                        max_x = 120
                x = random.randint(min_x,max_x - 32)
                y = random.randint(-220,-170)
                self.targets.append(Fuel(x,y))
                print('terrain was',bin(terrain),'fuel is on',x,y)
            #decide for enemies + level
        pass
    
    def update(self):
        #shoots
        for bullet in self.bullets[:]:
            bullet.update()
            if(bullet.y < 0):
                self.bullets.remove(bullet)
            for target in self.targets:
                if target.isAlive and self.check_collision(bullet,target):
                    self.bullets.remove(bullet)
                    target.isAlive = False
        #terrain
        self.update_terrain()
        self.check_collision_terrain()
        self.spawn_targets()
        #targets
        for target in self.targets[:]:
            if target.should_delete():
                self.targets.remove(target)
            target.update()
            if target.isAlive and self.check_collision(target,self.player):
                if not target.is_Ally:
                    self.player.isAlive = False
                else:
                    self.player.fuel += 20
                    if self.player.fuel > 1000: self.player.fuel = 1000
        self.player.fuel -=1
        if(not self.player.isAlive or self.player.fuel <= 0):
            self.state = 'gameover'
        
    def draw_background(self):
        display.set_pen(self.SKY_PEN)
        display.clear()
        
        display.set_pen(self.TERRAIN_PEN)
        
        for y,terrain in enumerate(self.terrain):
            coord_y = 200 - (y*120) + self.terrain_offset
            for x in range(0,8):
                if(terrain & (1 << x)):
                    display.rectangle(300-(20*x),coord_y, 20, 100)
                    display.rectangle(     20*x ,coord_y, 20, 100)
            if(coord_y > 0):
                dif =  abs((terrain & 0b111111) - (self.terrain[y+1] & 0b111111))
                match = terrain & self.terrain[y+1]
                xhign = 0
                xlow = 0
                for x in range(0,6):
                    if   dif & (1 << x): xhign = 20*(x + 1)
                    if match & (1 << x): xlow =  20*(x + 1)
                
                if((terrain& 0b111111) > (self.terrain[y+1]& 0b111111)):
                    temp = xhign
                    xhign = xlow
                    xlow = temp
                elif((terrain & 0b00111111) == (self.terrain[y+1] & 0b00111111)):
                    xhign = xlow
                    
                display.polygon([(  0,coord_y),(  0,coord_y-21),( -1 +xhign,coord_y-21),( -1 +xlow,coord_y)])
                display.polygon([(320,coord_y),(320,coord_y-21),(320 -xhign,coord_y-21),(320 -xlow,coord_y)])
                
                #special center slopes
                if   (not (terrain & 0b11000000) and     (self.terrain[y+1] & 0b11000000)): display.triangle(120,coord_y-21,200,coord_y-21,160,coord_y)
                elif (    (terrain & 0b11000000) and     (self.terrain[y+1] & 0b11000000)): display.rectangle(120,coord_y-21,80,21)
                elif (    (terrain & 0b11000000) and not (self.terrain[y+1] & 0b11000000)): display.triangle(120,coord_y,200,coord_y,160,coord_y-21)
        pass
    
    #draw
    def draw(self):
        self.draw_background()
        for bullet in self.bullets:
            bullet.draw()
        for target in self.targets:
            target.draw()
        self.player.draw()
        #wait 1/60s
    
game = Game()

random.seed(621)

while True:
    if(game.state == "playing"):
        game.process_input()
        #game.update()
        game.draw()
        game.update()
        display.update()
        time.sleep(0.01)
    if(game.state == "gameover"):
        display.set_pen(255)
        display.text("GAME OVER", 40, 35, 200, 7)
        display.update()
    
    
    