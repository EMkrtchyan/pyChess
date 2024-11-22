import pygame
import sys

import chess
# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800

bWIDTH, bHEIGHT = 142,142

bInsWIDTH, bInsHEIGHT = 128,128

scaleW = WIDTH//bWIDTH
scaleH = HEIGHT//bHEIGHT



startX, startY = scaleW*((bWIDTH-bInsWIDTH)//2),scaleH*((bHEIGHT-bInsHEIGHT)//2)
print(startX,startY)

endX, endY = WIDTH - startX, HEIGHT - startY

squareSize = (endX-startX)//8
print(squareSize)
# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Load board image
board = pygame.image.load("pixelChess/boards/board_plain_05.png")
board = pygame.transform.scale(board, (WIDTH, HEIGHT))


# Load cursor image
custom_cursor = pygame.image.load("pixelChess/cursor.png")

custom_cursor1 = custom_cursor.subsurface(pygame.Rect((0,0),(16,16)))
custom_cursor2 = custom_cursor.subsurface(pygame.Rect((16,0),(16,16)))
custom_cursor3 = custom_cursor.subsurface(pygame.Rect((32,0),(16,16)))


custom_cursor1 = pygame.transform.scale(custom_cursor1,(48,48))

cursor_width, cursor_height = custom_cursor1.get_size()

board1 = chess.board(scaleH,startX,startY,squareSize)
rook = chess.piece(0,0,"queen",True,scaleH)
# Hide the default cursor
pygame.mouse.set_visible(False)

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background
    screen.blit(board, (0, 0))
    

    # Get the current mouse position
    point = pygame.mouse.get_pos()
    point = (point[0] - cursor_width // 2, point[1] - cursor_height // 2)

    board1.draw(screen,point,custom_cursor1)

    # Draw the custom cursor
    screen.blit(custom_cursor1, (point[0], point[1]))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
