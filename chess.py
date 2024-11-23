
import pygame
# Screen dimensions
WIDTH, HEIGHT = 800, 800

bWIDTH, bHEIGHT = 142,142

bInsWIDTH, bInsHEIGHT = 128,128

scaleW = WIDTH//bWIDTH
scaleH = HEIGHT//bHEIGHT
startX, startY = scaleW*((bWIDTH-bInsWIDTH)//2),scaleH*((bHEIGHT-bInsHEIGHT)//2)

endX, endY = WIDTH - startX, HEIGHT - startY

squareSize = (endX-startX)//8


pieces = {"none":6,"pawn":0,"knight":1,"bishop":2,"rook":3,"queen":4,"king":5}
none = pygame.Surface((0,0))
bPawn = pygame.image.load("pixelChess/16x32/B_Pawn.png")
bKnight = pygame.image.load("pixelChess/16x32/B_Knight.png")
bBishop = pygame.image.load("pixelChess/16x32/B_Bishop.png")
bRook = pygame.image.load("pixelChess/16x32/B_Rook.png")
bQueen = pygame.image.load("pixelChess/16x32/B_Queen.png")
bKing = pygame.image.load("pixelChess/16x32/B_King.png")

bParr = [bPawn,bKnight,bBishop,bRook,bQueen,bKing,none]

wPawn = pygame.image.load("pixelChess/16x32/W_Pawn.png")
wKnight = pygame.image.load("pixelChess/16x32/W_Knight.png")
wBishop = pygame.image.load("pixelChess/16x32/W_Bishop.png")
wRook = pygame.image.load("pixelChess/16x32/W_Rook.png")
wQueen = pygame.image.load("pixelChess/16x32/W_Queen.png")
wKing = pygame.image.load("pixelChess/16x32/W_King.png")

wParr = [wPawn,wKnight,wBishop,wRook,wQueen,wKing,none]





def outline(img,loc,screen,size = 4):
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface()
    mask_surf.set_colorkey((0,0,0))
    screen.blit(mask_surf,(loc[0]-size,loc[1]))
    screen.blit(mask_surf,(loc[0]+size,loc[1]))
    screen.blit(mask_surf,(loc[0],loc[1]-size))
    screen.blit(mask_surf,(loc[0],loc[1]+size))

class piece:
    

    def __init__(self,x=0,y=0,type="pawn",white=True,scale = 1,startX=7,startY=7,squareSize=91):
        #types 6-none 0-pawn 1-knight 2-bishop 3-rook 4-queen 5-king
        self.x = x
        self.y = y
        self.scale = scale*0.8
        self.oline = False
        self.white = white
        self.type = pieces[type] 
        self.sprite = wParr[pieces[type]] if white else bParr[pieces[type]]
        self.sprite = pygame.transform.scale_by(self.sprite,self.scale)
        self.maskSprite = pygame.mask.from_surface(self.sprite)
        self.p_sizeX,self.p_sizeY = self.sprite.get_size()

        # self.posX = startX+x*squareSize+(squareSize-self.p_sizeX)//2
        # self.posY = startY+(y-1)*squareSize+(self.p_sizeY-squareSize)//4
        self.posX = startX+x*squareSize+squareSize//2
        self.posY = startY+y*squareSize+squareSize//2

        self.offsetX = self.p_sizeX//2
        self.offsetY = (self.p_sizeY//4)*3

    def draw(self,screen):
        if self.oline:
            outline(self.sprite,(self.posX-self.offsetX,self.posY-self.offsetY),screen)
        screen.blit(self.sprite,(self.posX-self.offsetX,self.posY-self.offsetY))


    def overlap(self,point,mouse):
        mouse1 = pygame.mask.from_surface(mouse)
        if self.maskSprite.overlap(mouse1,(point[0]-self.posX+self.offsetX,point[1]-self.posY+self.offsetY)):
            self.oline = True
            return True
        else:
            self.oline = False
            return False
        

    def posToCoord(self):
        return (max(min(int(self.posX+startX-squareSize)//squareSize,7),0),max(min((int(self.posY+startY-squareSize)//squareSize),7),0))
    def reCalculatePos(self):
        # self.posX = startX+self.x*squareSize+(squareSize-self.p_sizeX)//2
        # self.posY = startY+(self.y-1)*squareSize+(self.p_sizeY-squareSize)//4
        self.posX = startX+self.x*squareSize+squareSize//2
        self.posY = startY+self.y*squareSize+squareSize//2


class board:

    def __init__(self,scale=1,startX=14,startY=14,squareSize=91):
        self.mouseToX = 8
        self.mouseToY = 8
        self.scale = scale 
        self.curX = 8
        self.curY = 8
        self.curState=0
        self.lock = False
        self.canCastleW = True
        self.canCastleB = True
        self.whiteTurn = True
        self.Board = [
            [piece(0,0,"rook",False,scale,startX,startY,squareSize),piece(1,0,"knight",False,scale,startX,startY,squareSize),piece(2,0,"bishop",False,scale,startX,startY,squareSize),piece(3,0,"queen",False,scale,startX,startY,squareSize),piece(4,0,"king",False,scale,startX,startY,squareSize),piece(5,0,"bishop",False,scale,startX,startY,squareSize),piece(6,0,"knight",False,scale,startX,startY,squareSize),piece(7,0,"rook",False,scale,startX,startY,squareSize)],
            [piece(0,1,"pawn",False,scale,startX,startY,squareSize),piece(1,1,"pawn",False,scale,startX,startY,squareSize),piece(2,1,"pawn",False,scale,startX,startY,squareSize),piece(3,1,"pawn",False,scale,startX,startY,squareSize),piece(4,1,"pawn",False,scale,startX,startY,squareSize),piece(5,1,"pawn",False,scale,startX,startY,squareSize),piece(6,1,"pawn",False,scale,startX,startY,squareSize),piece(7,1,"pawn",False,scale,startX,startY,squareSize)],
            [piece(0,2,"none",False,scale,startX,startY,squareSize),piece(1,2,"none",False,scale,startX,startY,squareSize),piece(2,2,"none",False,scale,startX,startY,squareSize),piece(3,2,"none",False,scale,startX,startY,squareSize),piece(4,2,"none",False,scale,startX,startY,squareSize),piece(5,2,"none",False,scale,startX,startY,squareSize),piece(6,2,"none",False,scale,startX,startY,squareSize),piece(7,2,"none",False,scale,startX,startY,squareSize)],
            [piece(0,3,"none",False,scale,startX,startY,squareSize),piece(1,3,"none",False,scale,startX,startY,squareSize),piece(2,3,"none",False,scale,startX,startY,squareSize),piece(3,3,"none",False,scale,startX,startY,squareSize),piece(4,3,"none",False,scale,startX,startY,squareSize),piece(5,3,"none",False,scale,startX,startY,squareSize),piece(6,3,"none",False,scale,startX,startY,squareSize),piece(7,3,"none",False,scale,startX,startY,squareSize)],
            [piece(0,4,"none",False,scale,startX,startY,squareSize),piece(1,4,"none",False,scale,startX,startY,squareSize),piece(2,4,"none",False,scale,startX,startY,squareSize),piece(3,4,"none",False,scale,startX,startY,squareSize),piece(4,4,"none",False,scale,startX,startY,squareSize),piece(5,4,"none",False,scale,startX,startY,squareSize),piece(6,4,"none",False,scale,startX,startY,squareSize),piece(7,4,"none",False,scale,startX,startY,squareSize)],
            [piece(0,5,"none",False,scale,startX,startY,squareSize),piece(1,5,"none",False,scale,startX,startY,squareSize),piece(2,5,"none",False,scale,startX,startY,squareSize),piece(3,5,"none",False,scale,startX,startY,squareSize),piece(4,5,"none",False,scale,startX,startY,squareSize),piece(5,5,"none",False,scale,startX,startY,squareSize),piece(6,5,"none",False,scale,startX,startY,squareSize),piece(7,5,"none",False,scale,startX,startY,squareSize)],
            [piece(0,6,"pawn",True,scale,startX,startY,squareSize),piece(1,6,"pawn",True,scale,startX,startY,squareSize),piece(2,6,"pawn",True,scale,startX,startY,squareSize),piece(3,6,"pawn",True,scale,startX,startY,squareSize),piece(4,6,"pawn",True,scale,startX,startY,squareSize),piece(5,6,"pawn",True,scale,startX,startY,squareSize),piece(6,6,"pawn",True,scale,startX,startY,squareSize),piece(7,6,"pawn",True,scale,startX,startY,squareSize)],
            [piece(0,7,"rook",True,scale,startX,startY,squareSize),piece(1,7,"knight",True,scale,startX,startY,squareSize),piece(2,7,"bishop",True,scale,startX,startY,squareSize),piece(3,7,"queen",True,scale,startX,startY,squareSize),piece(4,7,"king",True,scale,startX,startY,squareSize),piece(5,7,"bishop",True,scale,startX,startY,squareSize),piece(6,7,"knight",True,scale,startX,startY,squareSize),piece(7,7,"rook",True,scale,startX,startY,squareSize)],
        ]
        self.wallBoard = [
            [True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True],
            [False,False,False,False,False,False,False,False],
            [False,False,False,False,False,False,False,False],
            [False,False,False,False,False,False,False,False],
            [False,False,False,False,False,False,False,False],
            [True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True]
        ]
    def draw(self,screen,point,mouse):
        if not self.curState == 2:
            self.curState = 0
        for row in self.Board:
            for elem in row:

                if elem.overlap(point,mouse):
                    self.mouseToX = elem.x
                    self.mouseToY = elem.y
                    if not self.curState == 2:
                        self.curState = 1
                elem.draw(screen)

    def pinch(self,point,drop = False):
        if self.mouseToX ==8 or self.Board[self.mouseToY][self.mouseToX].type == 6:
            #print("this")
            return
        if not self.lock:
            self.curState = 2
            self.lock = True
            self.curX = self.mouseToX
            self.curY = self.mouseToY
            self.Board[self.curY][self.curX].posX=point[0]
            self.Board[self.curY][self.curX].posY=point[1]
        else:
            if not drop:
                self.curState = 2
                # self.Board[self.curY][self.curX].posX=point[0]-self.Board[self.curY][self.curX].p_sizeX//2
                # self.Board[self.curY][self.curX].posY=point[1]-self.Board[self.curY][self.curX].p_sizeY//2
                self.Board[self.curY][self.curX].posX=point[0]
                self.Board[self.curY][self.curX].posY=point[1]
            else:
                self.curState = 1
                self.lock = False
                drop = False
                self.mouseToX = 8
                self.checkMove(self.curX,self.curY)
            #print(self.curState)
    def checkMove(self,x,y):
        dx,dy = self.Board[y][x].posToCoord()
        white = self.Board[y][x].white
        whiteTurn = self.whiteTurn
        if not (dx,dy) == (x,y) and white == whiteTurn:
            type = self.Board[y][x].type
            dtype = self.Board[dy][dx].type
            
            dwhite = self.Board[dy][dx].white
            match type:
                case 0:
                    if((dtype==6 and dx-x==0) and ((white and y-dy == 2 and y ==6) or (white and y-dy ==1) or (not white and dy-y==2 and y==1) or (not white and dy-y==1))):
                        self.move(x,y,dx,dy)
                        if(dy==7 or dy == 0):
                            self.Board[dy][dx] = piece(dx,dy,"queen",not self.whiteTurn,self.scale,startX,startY,squareSize)
                    
                    elif((not dtype==6 and abs(dx-x)==1 and not white == dwhite)and((white and y-dy==1)or(not white and dy-y==1))):
                        self.move(x,y,dx,dy)
                        if(dy==7 or dy == 0):
                            self.Board[dy][dx] = piece(dx,dy,"queen",not self.whiteTurn,self.scale,startX,startY,squareSize)
                case 1:
                    if(((abs(dx-x)==1 and abs(dy-y)==2) or (abs(dx-x)==2 and abs(dy-y)==1)) and (not white ==dwhite or dtype ==6) ):
                        self.move(x,y,dx,dy)
                case 2:
                    if(abs(dx-x)==abs(dy-y) and (not white == dwhite or dtype == 6)):
                        if raycast(x,y,dx,dy,self.wallBoard):
                            self.move(x,y,dx,dy)
                case 3:
                    if((dy-y == 0 or dx-x==0) and (not white == dwhite or dtype == 6)):
                        if raycast(x,y,dx,dy,self.wallBoard):
                            self.move(x,y,dx,dy)
                case 4:
                    if(abs(dx-x)==abs(dy-y) and (not white == dwhite or dtype == 6) or (dy-y == 0 or dx-x==0) and (not white == dwhite or dtype == 6)):
                        if raycast(x,y,dx,dy,self.wallBoard):
                            self.move(x,y,dx,dy)
                case 5:
                    if(max(abs(dy-y),abs(dx-x))<=1 and (not white == dwhite or dtype == 6)):
                        if self.whiteTurn:
                            self.canCastleW = False
                        else:
                            self.canCastleB = False
                        self.move(x,y,dx,dy)
                    elif(((self.canCastleW and self.whiteTurn) or (self.canCastleB and not self.whiteTurn)) and abs(dx-x)==2 and (dy-y)==0):
                        dir = int((dx-x)/abs(dx-x))
                        coordX = ((dir+1)//2)*7
                        
                        if not self.whiteTurn:
                            coordY = 0
                        else:
                            coordY = 7 
                        print(coordX,coordY)
                        if raycast(x,y,coordX,coordY,self.wallBoard):
                            self.move(x,y,dx,dy)
                            self.whiteTurn = not self.whiteTurn
                            self.move(coordX,coordY,dx-dir,dy)

                case _:
                    self.fullRec()
            #self.Board[dx][dy].reCalculatePos()
            self.fullRec()
        else:
            self.fullRec()
            #self.Board[dx][dy].reCalculatePos()
    def move(self,x,y,dx,dy):
            self.whiteTurn = not self.whiteTurn
            self.Board[dy][dx] = self.Board[y][x] 
            self.Board[dy][dx].x,self.Board[dy][dx].y = dx,dy
            self.Board[y][x] = piece(x,y,"none")
            self.wallBoard[y][x] = False
            self.wallBoard[dy][dx] = True
    def fullRec(self):
        for row in self.Board:
            for elem in row:
                elem.reCalculatePos()

def raycast(x,y,dx,dy,board):
    
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
        if not board[y+(i+1)*stepY][x+(i+1)*stepX] ==False:
            canGo = False
    return canGo
