import time
import sys

def animate(frames):
    c = 0
    for frame in frames:
        sys.stdout.write('\b\b\b')
        print("EPISODE:",c)
        sys.stdout.write(frame)
        sys.stdout.flush()
        time.sleep(0.1)
        c += 1
    sys.stdout.write('\rDone!     ')

def playGrid(frames):
    import pygame
    first = frames[0]
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    n = len(first)
    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 20
    HEIGHT = 20

    # This sets the margin between each cell
    MARGIN = 5

    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.
    # Initialize pygame
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [1000, 1000]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("Array Backed Grid")
    # -------- Main Program Loop -----------
        # Set the screen background
    for i in range(len(frames)):
        frame = frames[i]
        for event in pygame.event.get():
            pass
        screen.fill(BLACK)
        for row in range(n):
            for column in range(n):
                color = WHITE
                # print(row,column)
                if frame[row][column] == 1:
                    color = GREEN
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        # Limit to 60 frames per second
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
