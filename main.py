import pygame
import sys


# Screen dimensions
WIDTH, HEIGHT = 800, 800

bWIDTH, bHEIGHT = 142,142

bInsWIDTH, bInsHEIGHT = 128,128

scaleW = WIDTH//bWIDTH
scaleH = HEIGHT//bHEIGHT
startX, startY = scaleW*((bWIDTH-bInsWIDTH)//2),scaleH*((bHEIGHT-bInsHEIGHT)//2)

endX, endY = WIDTH - startX, HEIGHT - startY

squareSize = (endX-startX)//8


#pieces = {"none":6,"pawn":0,"knight":1,"bishop":2,"rook":3,"queen":4,"king":5}
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

pieces = {'p':bPawn,'n':bKnight,'b':bBishop,'r':bRook,'q':bQueen,'k':bKing,'P':wPawn,'N':wKnight,'B':wBishop,'R':wRook,'Q':wQueen,'K':wKing}

for piece in pieces:
    pieces[piece] = pygame.transform.scale_by(pieces[piece],scaleH*0.8)

def outline(img,loc,screen,size = 4):
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface()
    mask_surf.set_colorkey((0,0,0))
    screen.blit(mask_surf,(loc[0]-size,loc[1]))
    screen.blit(mask_surf,(loc[0]+size,loc[1]))
    screen.blit(mask_surf,(loc[0],loc[1]-size))
    screen.blit(mask_surf,(loc[0],loc[1]+size))

class piece:
    
    def __init__(self,x=0,y=0,type="P"):
        #types 6-none 0-pawn 1-knight 2-bishop 3-rook 4-queen 5-king
        self.x = x
        self.y = y
        self.oline = False
        self.white = type.isupper()
        self.type = type
        self.sprite = pieces[type] 
        self.p_sizeX,self.p_sizeY = self.sprite.get_size()
        self.allMoves = set()

        

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
        
    def __repr__(self):
        return self.type +f"({self.x},{self.y})"

    def posToCoord(self):
        return (max(min(int(self.posX+startX-squareSize)//squareSize,7),0),max(min((int(self.posY+startY-squareSize)//squareSize),7),0))
    def reCalculatePos(self):
        # self.posX = startX+self.x*squareSize+(squareSize-self.p_sizeX)//2
        # self.posY = startY+(self.y-1)*squareSize+(self.p_sizeY-squareSize)//4
        self.posX = startX+self.x*squareSize+squareSize//2
        self.posY = startY+self.y*squareSize+squareSize//2



class board:

    def __init__(self,screen,fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq -"):
        self.curState = 0
        self.screen = screen
        self.lock = False
        self.fens = fen.split(' ')
        self.whiteToMove = True
        self.blockSquare = [[False for i in range(8)] for j in range(8)]
        self.pieces = self.fenToList(self.fens[0])
        self.cur=0
        self.onP = False

        self.canCastleW = "K" in self.fens[2] or "Q" in self.fens[2]
        self.canCastleB = "k" in self.fens[2] or "q" in self.fens[2]

        for piece in self.pieces:
            self.checkMoves(piece)
        pass

    def oline(self,XY):
        x = XY[0]
        y = XY[1]
        if not self.lock:
            for p in self.pieces:
                p.oline = False
            self.onP = False
            self.cur = self.coordToIdx(x,y)
            
            if not self.blockSquare[y][x] == False:
                self.pieces[self.cur].oline = True
                self.onP = True 
            
            else:
                self.pieces[self.cur].oline = False
        else:
            self.pieces[self.cur].oline = True 

    def pinch(self,point,drop = False):
        #self.pieces[self.cur].posX,self.pieces[self.cur].posY = point

        if not self.lock and self.onP:

            self.curState = 2
            self.lock = True
            self.pieces[self.cur].posX,self.pieces[self.cur].posY = point
            print(self.pieces[self.cur].allMoves)
        else:
            if not drop and self.onP:
                self.curState = 2
                # self.Board[self.curY][self.curX].posX=point[0]-self.Board[self.curY][self.curX].p_sizeX//2
                # self.Board[self.curY][self.curX].posY=point[1]-self.Board[self.curY][self.curX].p_sizeY//2
                self.pieces[self.cur].posX,self.pieces[self.cur].posY = point
            else:
                self.curState = 1
                self.lock = False
                drop = False
                self.mouseToX = 8
                dXY = pointToXY(point)
                #print(dXY,self.pieces[self.cur].allMoves)
                if dXY in self.pieces[self.cur].allMoves:
                    self.move(dXY)
                else:
                    self.fullRec()
    def fullRec(self):
        for elem in self.pieces:
            elem.reCalculatePos()
        for piece in self.pieces:
            self.checkMoves(piece)
        
    def checkMoves(self,piece):
        white = piece.white
        whiteTurn = self.fens[1] == "w"
        x,y = piece.x,piece.y
        for dy in range(8):
            for dx in range(8):
                if not (dx,dy) == (x,y) and white == whiteTurn:
                    type1 = piece.type
                    dIdx =self.coordToIdx(dx,dy)
                    print(dIdx)
                    if not dIdx == False:
                        dtype = self.pieces[dIdx].type
                        dwhite = self.pieces[dIdx].white
                    else:
                        dtype =False
                        dwhite = False
                    
                    
                    
                        if self.fens[1] == "b":
                            if type1 == 'p':
                                print(type1,dtype)
                                if((dtype==False and dx-x==0) and ((dy-y==2 and y==1) or (dy-y==1))):
                                    piece.allMoves.add((dx,dy))
                                    if(dy==7 or dy == 0):
                                        piece.type = 'q'
                                
                                elif((not dtype==False and abs(dx-x)==1 and dwhite)and((dy-y==1))):
                                    piece.allMoves.add((dx,dy))
                                    if(dy==7 or dy == 0):
                                        piece.type = 'q'
                            if type1 == 'n':
                                if(((abs(dx-x)==1 and abs(dy-y)==2) or (abs(dx-x)==2 and abs(dy-y)==1)) and (not white ==dwhite or dtype == False) ):
                                    piece.allMoves.add((dx,dy))
                            if type1 == 'b':
                                if(abs(dx-x)==abs(dy-y) and (not white == dwhite or dtype == False)):
                                    if raycast(x,y,dx,dy,self.blockSquare):
                                        piece.allMoves.add((dx,dy))
                            if type1 == 'r':
                                if((dy-y == 0 or dx-x==0) and (not white == dwhite or dtype == False)):
                                    if raycast(x,y,dx,dy,self.blockSquare):
                                        piece.allMoves.add((dx,dy))
                            if type1 == 'q':
                                if(abs(dx-x)==abs(dy-y) and (not white == dwhite or dtype == False) or (dy-y == 0 or dx-x==0) and (not white == dwhite or dtype == False)):
                                    if raycast(x,y,dx,dy,self.blockSquare):
                                        piece.allMoves.add((dx,dy))
                            if type1 == 'k':
                                if(max(abs(dy-y),abs(dx-x))<=1 and (not white == dwhite or dtype == False)):
                                    if self.whiteToMove:
                                        self.canCastleW = False
                                    else:
                                        self.canCastleB = False
                                    piece.allMoves.add((dx,dy))
                                elif(((self.canCastleW and self.whiteToMove) or (self.canCastleB and not self.whiteToMove)) and abs(dx-x)==2 and (dy-y)==0):
                                    dir = int((dx-x)/abs(dx-x))
                                    coordX = ((dir+1)//2)*7
                                    
                                    if not self.whiteToMove:
                                        coordY = 0
                                    else:
                                        coordY = 7 
                                    #print(coordX,coordY)
                                    if raycast(x,y,coordX,coordY,self.blockSquare):
                                        piece.allMoves.add((dx,dy))
                                        self.whiteToMove = not self.whiteToMove
                                        self.move(coordX,coordY,dx-dir,dy)
                        else:
                            if type1 == 'P':
                                if((dtype==False and dx-x==0) and ((dy-y==2 and y==1) or (dy-y==1))):
                                    piece.allMoves.add((dx,dy))
                                    if(dy==7 or dy == 0):
                                        piece.type = 'q'
                                
                                elif((not dtype==False and abs(dx-x)==1 and not white == dwhite)and((dy-y==1))):
                                    piece.allMoves.add((dx,dy))
                                    if(dy==7 or dy == 0):
                                        piece.type = 'q'
                            if type1 == 'P':
                                if(((abs(dx-x)==1 and abs(dy-y)==2) or (abs(dx-x)==2 and abs(dy-y)==1)) and (not white ==dwhite or dtype == False) ):
                                    piece.allMoves.add((dx,dy))
                            if type1 == 'B':
                                if(abs(dx-x)==abs(dy-y) and (not white == dwhite or dtype == False)):
                                    if raycast(x,y,dx,dy,self.blockSquare):
                                        piece.allMoves.add((dx,dy))
                            if type1 == 'R':
                                if((dy-y == 0 or dx-x==0) and (not white == dwhite or dtype == False)):
                                    if raycast(x,y,dx,dy,self.blockSquare):
                                        piece.allMoves.add((dx,dy))
                            if type1 == 'Q':
                                if(abs(dx-x)==abs(dy-y) and (not white == dwhite or dtype == False) or (dy-y == 0 or dx-x==0) and (not white == dwhite or dtype == False)):
                                    if raycast(x,y,dx,dy,self.blockSquare):
                                        piece.allMoves.add((dx,dy))
                            if type1 == 'K':
                                if(max(abs(dy-y),abs(dx-x))<=1 and (not white == dwhite or dtype == False)):
                                    if self.whiteToMove:
                                        self.canCastleW = False
                                    else:
                                        self.canCastleB = False
                                    piece.allMoves.add((dx,dy))
                                elif(((self.canCastleW and self.whiteToMove) or (self.canCastleB and not self.whiteToMove)) and abs(dx-x)==2 and (dy-y)==0):
                                    dir = int((dx-x)/abs(dx-x))
                                    coordX = ((dir+1)//2)*7
                                    
                                    if not self.whiteToMove:
                                        coordY = 0
                                    else:
                                        coordY = 7 
                                    #print(coordX,coordY)
                                    if raycast(x,y,coordX,coordY,self.blockSquare):
                                        piece.allMoves.add((dx,dy))
                                        self.whiteToMove = not self.whiteToMove
                                        self.move(coordX,coordY,dx-dir,dy)

                            
                    #self.fullRec()
                    #self.Board[dx][dy].reCalculatePos()
    def move(self,dXY):
        x,y = self.pieces[self.cur].x,self.pieces[self.cur].y
        dX,dY = dXY[0],dXY[1]
        if self.fens[1] == "w":
            self.fens[1] = "b"
        else:
            self.fens[1] = "w"
        print(self.fens[1])
        if not self.blockSquare[dY][dX] == False:
            del self.pieces[self.coordToIdx(dX,dY)]
        del self.pieces[self.coordToIdx(x,y)]
        self.blockSquare[dY][dX] = self.blockSquare[y][x]
        self.blockSquare[y][x] = False 
        #print(self.blockSquare[dY][dX])
        #print(dY,dX,x,y)
        self.pieces.append(piece(dX,dY,self.blockSquare[dY][dX]))
        self.fullRec()

        for row in self.blockSquare:
            print(row)


    
    def coordToIdx(self,x,y):
        for i,p in enumerate(self.pieces):
            if (p.x,p.y) == (x,y):
                return i
        return False


    def darkSquare(self,x,y):
        s = pygame.Surface((squareSize,squareSize))  
        s.set_alpha(128)             
        s.fill((0,0,0))          
        self.screen.blit(s, (startX+(squareSize-1)*x+5,startY+(squareSize-1)*y+5))   
        
    def fenToList(self,fen):
        rows = fen.split("/")
        pieces = list()
        for y,row in enumerate(rows):
            contDigit = False
            for x,piece_c in enumerate(row):
                if piece_c.isdigit():
                    x+=int(piece_c)
                    contDigit = True
                    #print(x)
                else:
                    pieces.append(piece(x,y,piece_c))
                    self.blockSquare[y][x] = piece_c
        
        for row in self.blockSquare:
            print(row)
        return pieces
        


    def draw(self,point,a):
        self.screen.blit(boardIm,(0,0))
        for p in self.pieces:
            p.draw(self.screen)
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
        #print(y+(i)*stepY,min(7,x+(i)*stepX))
        if not board[min(7,y+(i+1)*stepY)][min(7,x+(i+1)*stepX)] == False:
            canGo = False
    return canGo

pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")


pygame.mixer.music.load("./sounds/mozart.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Load board image
boardIm = pygame.image.load("pixelChess/boards/board_plain_05.png")
boardIm = pygame.transform.scale(boardIm, (WIDTH, HEIGHT))


# Load cursor image
custom_cursor = pygame.image.load("pixelChess/cursor.png")

custom_cursor1 = custom_cursor.subsurface(pygame.Rect((0,0,16,16)))
custom_cursor2 = custom_cursor.subsurface(pygame.Rect((16,0,16,16)))
custom_cursor3 = custom_cursor.subsurface(pygame.Rect((32,0,16,16)))

#regs = {(0,0,)}


custom_cursor1 = pygame.transform.scale(custom_cursor1,(48,48))
custom_cursor2 = pygame.transform.scale(custom_cursor2,(48,48))
custom_cursor3 = pygame.transform.scale(custom_cursor3,(48,48))

cursors=[custom_cursor1,custom_cursor2,custom_cursor3]

cursor_width, cursor_height = custom_cursor1.get_size()

board1 = board(screen)

# Hide the default cursor
pygame.mouse.set_visible(False)

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()


def pointToXY(point):
    X = point[0]-startX
    Y = point[1]-startY
    X//=squareSize
    Y//=squareSize
    return(max(0,min(X,7)),max(0,min(Y,7)))

# Game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     point1 = pygame.mouse.get_pos()
        #     board1.pinch(point1)
        # if event.type == pygame.MOUSEBUTTONUP:
        #     point1 = pygame.mouse.get_pos()
        #     board1.pinch(point1,True)
        if pygame.mouse.get_pressed()[0]:
            try:
                point1 = pygame.mouse.get_pos()
                board1.pinch(point1)
            except AttributeError:
                pass    
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                point1 = pygame.mouse.get_pos()
                board1.pinch(point1,True)

    

    # Get the current mouse position
    point = pygame.mouse.get_pos()
    

    point = (point[0] - cursor_width // 2, point[1] - cursor_height // 2)

    board1.draw(point,cursors[board1.curState])

    board1.oline(pointToXY(point))

    screen.blit(cursors[board1.curState], (point[0], point[1]))
    

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()



