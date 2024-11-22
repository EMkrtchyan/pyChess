
import pygame

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


class piece:
    

    def __init__(self,x=0,y=0,type="pawn",white=True,scale = 1,startX=7,startY=7,squareSize=91):
        #types 6-none 0-pawn 1-knight 2-bishop 3-rook 4-queen 5-king
        self.x = x
        self.y = y
        self.scale = scale
        
        self.white = white
        self.type = pieces[type] 
        self.sprite = wParr[pieces[type]] if white else bParr[pieces[type]]
        self.sprite = pygame.transform.scale_by(self.sprite,scale)
        self.p_sizeX,self.p_sizeY = self.sprite.get_size()

        self.posX = startX+x*squareSize+(squareSize-self.p_sizeX)//2
        self.posY = startY+(y-1)*squareSize+(self.p_sizeY-squareSize)//4

    def draw(self,screen):
        screen.blit(self.sprite,(self.posX,self.posY))

class board:

    def __init__(self,scale=1,startX=14,startY=14,squareSize=91):
        self.canCastle = True
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
    def draw(self,screen):
        for row in self.Board:
            for elem in row:
                elem.draw(screen)