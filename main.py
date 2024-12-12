#boar parent class
class Board():
    def __init__(self):
        self.b =[
            ["r","b","n","q","k","n","b","r"],
            ["p","p","p","p","p","p","p","p"],
            ["e","e","e","e","e","e","e","e"],
            ["e","e","e","e","e","e","e","e"],
            ["e","e","e","e","e","e","e","e"],
            ["e","e","e","e","e","e","e","e"],
            ["P","P","P","P","P","P","P","P"],
            ["R","B","N","Q","K","N","B","R"]
        ]
        self.m = [[set() for i in range(8)] for j in range(8)]
        self.checkBoard()
    
    def checkBoard(self):
        for x in range(8):
            for y in range(8):
                self.checkMoves(x,y)
    
    def checkMoves(self,x,y):
        elem = self.b[y][x]
        if elem=="e":
            return
        for dy in range(8):
            for dx in range(8):
                if not (dy,dx) == (x,y):
                    self.checkMove(x,y,dx,dy)
    
    def checkMove(self,x,y,dx,dy):
        elem = self.b[y][x]
        delem = self.b[dy][dx]
        if elem.isupper() and not delem.isupper():
            if elem == "P":
                if ((x-dx==0 and (y-dy==1 or (y-dy==2 and y==6))) or (abs(x-dx)==1 and y-dy==1 and not delem=="e")):
                    self.m[y][x].add((dy,dx))
            
            if elem == "N":
                if ((abs(dx-x)==1 and abs(dy-y)==2) or (abs(dx-x)==2 and abs(dy-y)==1)):
                    self.m[y][x].add((dy,dx))
                    
            if elem == "B":
                if abs(dx-x)==abs(dy-y) and self.ray(x,y,dx,dy):
                    self.m[y][x].add((dy,dx))
                    
            if elem == "R":
                if (dy-y == 0 or dx-x==0) and self.ray(x,y,dx,dy):
                    self.m[y][x].add((dy,dx))
                    
            if elem == "Q":
                if (dy-y == 0 or dx-x==0) or abs(dx-x)==abs(dy-y) and self.ray(x,y,dx,dy):
                    self.m[y][x].add((dy,dx))
                    
            if elem == "K":
                if (max(abs(dy-y),abs(dx-x))<=1):
                    self.m[y][x].add((dy,dx))
        elif elem.islower() and (not delem.islower() or delem =="e"):
            if elem == "p":
                if ((x-dx==0 and (dy-y==1 or (dy-y==2 and y==1))) or (abs(x-dx)==1 and dy-y==1 and not self.b[dy][dx]=="e")):
                    self.m[y][x].add((dy,dx))
            
            if elem == "n":
                if ((abs(dx-x)==1 and abs(dy-y)==2) or (abs(dx-x)==2 and abs(dy-y)==1)):
                    self.m[y][x].add((dy,dx))
                    
            if elem == "b":
                if abs(dx-x)==abs(dy-y) and self.ray(x,y,dx,dy):
                    self.m[y][x].add((dy,dx))
                    
            if elem == "r":
                if (dy-y == 0 or dx-x==0) and self.ray(x,y,dx,dy):
                    self.m[y][x].add((dy,dx))
                    
            if elem == "q":
                if (dy-y == 0 or dx-x==0) or abs(dx-x)==abs(dy-y) and self.ray(x,y,dx,dy):
                    self.m[y][x].add((dy,dx))
                    
            if elem == "k":
                if (max(abs(dy-y),abs(dx-x))<=1):
                    self.m[y][x].add((dy,dx))
    def ray(self,x,y,dx,dy):
        if(dx-x==0):
            stepX = 0
        else:
            stepX = (dx-x)//abs(dx-x)
        if(dy-y==0):
            stepY = 0
        else:
            stepY = (dy-y)//abs(dy-y)
        canGo = True 
        for i in range(max(abs(dx-x),abs(dy-y))-1):
            if not self.b[y+(i+1)*stepY][x+(i+1)*stepX] =="e":
                canGo = False
        return canGo
    
    def move(self,x,y,dx,dy):
        if (dy,dx) in self.m[y][x]:
            temp = self.b[y][x]
            self.b[y][x] = "e"
            self.b[dy][dx] = temp
            self.m = [[set() for i in range(8)] for j in range(8)]
            self.checkBoard()
        else:
            print("not a valid move")
        
    def __repr__(self):
        repres = ""
        for y in range(8):
            for x in range(8):
                repres+=" "+self.b[y][x]+" "
            repres+="\n"
        return repres





class BoardSurf(Board):
    def __init__(self,width,height):
        super().__init__()
        self.posX = 0
        self.posY = 0
        self.mouseX = 0
        self.mouseY = 0
        
        self.Surf = boardSurf.copy()
        self.highlightSurf = pg.Surface((width,height),pg.SRCALPHA, 32)
        #self.highlightSurf = self.highlightSurf.convert_alpha
        self.highlightSurf.fill(empty)
        self.rect = pg.Rect(self.posX,self.posY,width,height)
        self.squareW = width//8
        self.squareH = height//8
        self.pinched = False
        self.hitX = 0
        self.hitY = 0
        self.update()
        
    def draw(self,screen):
        screen.blit(self.Surf,(self.posX,self.posY))
        screen.blit(self.highlightSurf,(self.posX,self.posY))
        if self.pinched:
            screen.blit(self.pinched[2],(self.mouseX-pieceW//2,self.mouseY-pieceH//1.5))
    
    def update(self):
        self.Surf = boardSurf.copy()
        for y,row in enumerate(self.b):
            for x,piece in enumerate(row):
                if not piece == "e":                    
                    self.Surf.blit(pieces[piece],(self.squareW*x+startX,self.squareH*y+startY))
                    
    def pinch(self,x,y):
        if self.pinched:
            return
        if self.b[y][x]=="e":
            return
        
        self.pinched = ((x,y),self.b[y][x],pieces[self.b[y][x]])
        self.b[y][x] = "e"
        self.update()
    
    def release(self):
        if self.pinched:
            pos, pieceT = (self.pinched[0], self.pinched[1])
            self.pinched = False
            x,y = pos
            self.b[y][x] = pieceT
            self.move(x,y,self.hitX,self.hitY)
            #print(x,y,self.hitX,self.hitY)
            self.checkBoard()
            self.update()
        
        
    def highlight(self,x,y,size = 4):
        piece = self.b[y][x]
        if piece == "e":
            self.highlightSurf.fill(empty)
            return
        sprite = pieces[piece]
        mask = pg.mask.from_surface(sprite)
        mask_surf = mask.to_surface()
        mask_surf.set_colorkey((0,0,0))
        self.highlightSurf.fill(empty)
        self.highlightSurf.blit(mask_surf,(self.squareW*x+startX-size,self.squareH*y+startY))
        self.highlightSurf.blit(mask_surf,(self.squareW*x+startX+size,self.squareH*y+startY))
        self.highlightSurf.blit(mask_surf,(self.squareW*x+startX,self.squareH*y+startY-size))
        self.highlightSurf.blit(mask_surf,(self.squareW*x+startX,self.squareH*y+startY+size))
        self.highlightSurf.blit(sprite,(self.squareW*x+startX,self.squareH*y+startY))
            
    
                


import pygame as pg
import sys

empty = pg.Color(0,0,0,0)

resolution = (800,800)
width = resolution[0]
height = resolution[1]
squareW = width//8
squareH = height//8

boardSurf = pg.transform.scale(pg.image.load('Sprites/Board.png'),(width,height))

# bPawn = pg.image.load("Sprites/16x32/B_Pawn.png")
# bKnight = pg.image.load("Sprites/16x32/B_Knight.png")
# bBishop = pg.image.load("Sprites/16x32/B_Bishop.png")
# bRook = pg.image.load("Sprites/16x32/B_Rook.png")
# bQueen = pg.image.load("Sprites/16x32/B_Queen.png")
# bKing = pg.image.load("Sprites/16x32/B_King.png")

# wPawn = pg.image.load("Sprites/16x32/W_Pawn.png")
# wKnight = pg.image.load("Sprites/16x32/W_Knight.png")
# wBishop = pg.image.load("Sprites/16x32/W_Bishop.png")
# wRook = pg.image.load("Sprites/16x32/W_Rook.png")
# wQueen = pg.image.load("Sprites/16x32/W_Queen.png")
# wKing = pg.image.load("Sprites/16x32/W_King.png")

WhiteSpite = pg.image.load("Sprites/16x16/WhitePieces.png")
BlackSpite = pg.image.load("Sprites/16x16/BlackPieces.png")

bPawn = BlackSpite.subsurface(pg.Rect((0,0,16,16)))
bKnight = BlackSpite.subsurface(pg.Rect((16,0,16,16)))
bBishop = BlackSpite.subsurface(pg.Rect((48,0,16,16)))
bRook = BlackSpite.subsurface(pg.Rect((32,0,16,16)))
bQueen = BlackSpite.subsurface(pg.Rect((64,0,16,16)))
bKing = BlackSpite.subsurface(pg.Rect((80,0,16,16)))

wPawn = WhiteSpite.subsurface(pg.Rect((0,0,16,16)))
wKnight = WhiteSpite.subsurface(pg.Rect((16,0,16,16)))
wBishop = WhiteSpite.subsurface(pg.Rect((48,0,16,16)))
wRook = WhiteSpite.subsurface(pg.Rect((32,0,16,16)))
wQueen = WhiteSpite.subsurface(pg.Rect((64,0,16,16)))
wKing = WhiteSpite.subsurface(pg.Rect((80,0,16,16)))



pieces = {"p":bPawn,"n":bKnight,"b":bBishop,"r":bRook,"q":bQueen,"k":bKing,"P":wPawn,"N":wKnight,"B":wBishop,"R":wRook,"Q":wQueen,"K":wKing}

scaleF = 0.8*min(squareW//16,squareH//16)
pieceW = scaleF*16
pieceH = scaleF*16
startX = (squareW-pieceW)//2
startY = (squareW-pieceH)//2

for piece in pieces:
    pieces[piece] = pg.transform.scale_by(pieces[piece],scaleF)

# Load cursor image
custom_cursor = pg.image.load("Sprites/cursor.png")

custom_cursor1 = custom_cursor.subsurface(pg.Rect((0,0,16,16)))
custom_cursor2 = custom_cursor.subsurface(pg.Rect((16,0,16,16)))
custom_cursor3 = custom_cursor.subsurface(pg.Rect((32,0,16,16)))

cursors=[custom_cursor1,custom_cursor2,custom_cursor3]

for cursor in cursors:
    cursor = pg.transform.scale(cursor,(48,48))


# initializing imported module
pg.init()

pg.mixer.music.load("./Sounds/mozart.mp3")
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(-1)


# displaying a window of height
# 500 and width 400
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()

brd = BoardSurf(width,height)
# Setting name for window
pg.display.set_caption('pyChess')

# creating a bool value which checks 
# if game is running
running = True

# Game loop
# keep game running till running is true
while running:
    # Check for event if user has pushed 
    # any event in queue
    
    
    for event in pg.event.get():
        
        if event.type == pg.MOUSEMOTION:
            x, y = event.pos
            if brd.rect.collidepoint(event.pos):
                brd.mouseX = (x - brd.rect.x)
                brd.mouseY = (y - brd.rect.y)
                brd.hitX = (x - brd.rect.x)//squareW
                brd.hitY = (y - brd.rect.y)//squareH
                brd.highlight(brd.hitX,brd.hitY)
        # if pg.mouse.get_pressed()[0]:
        #     brd.pinch(brd.hitX,brd.hitY)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                brd.pinch(brd.hitX,brd.hitY)  
        
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                brd.release()
        # if event is of type quit then set
        # running bool to false
        if event.type == pg.QUIT:
            running = False
            
    brd.draw(screen)     
    # Update the display
    pg.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)


# Quit Pygame
pg.quit()
sys.exit()