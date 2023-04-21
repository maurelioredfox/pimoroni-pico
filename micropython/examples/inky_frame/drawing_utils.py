#some constants for the colors
BLACK = 0
WHITE = 1
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6
TAUPE = 7

class ColorDither:
    
    def __init__(self,display):
        self.graphics = display


    def __drawRectangle2Colors(self,x0,y0,xLength,yLength,colors):
        
        self.graphics.set_pen(colors[1])
        for x in range(x0, x0+xLength):
            for y in range(y0, y0+yLength):
                if ((x + y) % 2 == 0):
                    self.graphics.pixel(x, y)

    def __drawRectangle3Colors(self,x0,y0,xLength,yLength,colors):
        
        self.graphics.set_pen(colors[1])
        for x in range(x0, x0+xLength):
            for y in range(y0, y0+yLength):
                if ((x + y) % 3 == 0):
                    self.graphics.pixel(x, y)
                    
        self.graphics.set_pen(colors[2])
        for x in range(x0, x0+xLength):
            for y in range(y0, y0+yLength):
                if ((x + y) % 3 == 1):
                    self.graphics.pixel(x, y)
        
    def __drawRectangle4Colors(self,x0,y0,xLength,yLength,colors):
        
        self.graphics.set_pen(colors[1])
        for x in range(x0, x0+xLength):
            for y in range(y0, y0+yLength):
                if (y % 2 == 0 and x % 2 == 1):
                    self.graphics.pixel(x, y)
                    
        self.graphics.set_pen(colors[2])
        for x in range(x0, x0+xLength):
            for y in range(y0, y0+yLength):
                if (y % 2 == 1 and x % 2 == 0):
                    self.graphics.pixel(x, y)
                    
        self.graphics.set_pen(colors[3])
        for x in range(x0, x0+xLength):
            for y in range(y0, y0+yLength):
                if (y % 2 == 1 and x % 2 == 1):
                    self.graphics.pixel(x, y)
        

    def drawRectangleColors(self,x0,y0,xLength,yLength,colors):
        
        self.graphics.set_pen(colors[0])
        self.graphics.rectangle(x0, y0, xLength, yLength)
        
        if len(colors) == 1:
            pass
        elif len(colors) == 2:
            self.__drawRectangle2Colors(x0,y0,xLength,yLength,colors)
        elif len(colors) == 3:
            self.__drawRectangle3Colors(x0,y0,xLength,yLength,colors)
        elif len(colors) == 4:
            self.__drawRectangle4Colors(x0,y0,xLength,yLength,colors)
        else:
            raise Exception("unsupported aumont of colors")
    
    dither_matrix_7_16 = \
    [[0,0,1,0],
     [0,1,0,1],
     [1,0,1,0],
     [0,1,0,1]]
    
    dither_matrix_6_16 = \
    [[0,0,1,0],
     [0,1,0,1],
     [1,0,0,0],
     [0,1,0,1]]
    
    dither_matrix_5_16 = \
    [[0,0,0,0],
     [0,1,0,1],
     [0,0,1,0],
     [0,1,0,1]]
    
    dither_matrix_4_16 = \
    [[0,0,0,0],
     [0,1,0,1],
     [0,0,0,0],
     [0,1,0,1]]
    
    dither_matrix_3_16 = \
    [[0,0,0,0],
     [0,1,0,1],
     [0,0,0,0],
     [0,1,0,0]]
    
    dither_matrix_2_16 = \
    [[0,0,0,0],
     [0,0,0,1],
     [0,0,0,0],
     [0,1,0,0]]
    
    dither_matrix_1_16 = \
    [[0,0,0,0],
     [0,1,0,0],
     [0,0,0,0],
     [0,0,0,0]]

    
    def drawRectangleDithering(self,x0,y0,xLength,yLength,color1,color2,dither):
        
        if dither is 1:
            matrix = self.dither_matrix_1_16
        elif dither is 2:
            matrix = self.dither_matrix_2_16
        elif dither is 3:
            matrix = self.dither_matrix_3_16
        elif dither is 4:
            matrix = self.dither_matrix_4_16
        elif dither is 5:
            matrix = self.dither_matrix_5_16
        elif dither is 6:
            matrix = self.dither_matrix_6_16
        elif dither is 7:
            matrix = self.dither_matrix_7_16
        else:
            raise Exception("unsupported dithering table")
        
        self.graphics.set_pen(color1)
        self.graphics.rectangle(x0, y0, xLength, yLength)
        
        self.graphics.set_pen(color2)
        
        for x in range(x0,x0+xLength):
            for y in range(y0,y0+yLength):
                if(matrix[x % 4][y % 4] == 1):
                    self.graphics.pixel(x,y)
        
