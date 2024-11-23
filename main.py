import pygame
import sys

import chess
# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = chess.WIDTH,chess.HEIGHT

bWIDTH, bHEIGHT = chess.bWIDTH,chess.bHEIGHT

bInsWIDTH, bInsHEIGHT = chess.bInsWIDTH,chess.bInsHEIGHT

scaleW, scaleH  = chess.scaleW, chess.scaleH

startX, startY = chess.startX, chess.startY
endX, endY = chess.endX, chess.endY

squareSize = chess.squareSize
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
custom_cursor2 = pygame.transform.scale(custom_cursor2,(48,48))
custom_cursor3 = pygame.transform.scale(custom_cursor3,(48,48))

cursors=[custom_cursor1,custom_cursor2,custom_cursor3]

cursor_width, cursor_height = custom_cursor1.get_size()

board1 = chess.board(scaleH,startX,startY,squareSize)
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
