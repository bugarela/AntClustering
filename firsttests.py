from random import random, randint
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# This sets the margin between each cell
MARGIN = 2

N = 100
n_dead = 700

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 5
HEIGHT = 5

vision_field = 8

class Ant():
    def __init__(self, size):
        self.x = int(random() * size)
        self.y = int(random() * size)
        self.state = 0
    def move(self, size):
        self.x = max(min(self.x + randint(-1,1), size-1), 0)
        self.y = max(min(self.y + randint(-1,1), size-1), 0)


def generate_grid(size=100):
    return [[0 for _ in range(size)] for _ in range(size)]

def spreads_itens(grid, n_itens):
    i = 0
    j = 0
    for _ in range(n_itens):
        while(grid[i][j] != 0):
            i = int(random() * len(grid))
            j = int(random() * len(grid))
        grid[i][j] = 1
    return grid

test_grid = generate_grid(N)
grid = generate_grid(N)
dead_ants = spreads_itens(test_grid, n_dead)

ant1 = Ant(N)
grid[ant1.x][ant1.y] -= 1
ant1.move(N)
grid[ant1.x][ant1.y] += 1
pygame.init()

WINDOW_SIZE = [N * (WIDTH + MARGIN), N * (HEIGHT + MARGIN)]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Array Backed Grid")
done = False
clock = pygame.time.Clock()

screen.fill(BLACK)

while(not done):
    # Draw the grid
    for row in range(N):
        for column in range(N):
            color = BLACK
            if dead_ants[row][column] == 1:
                color = WHITE
            if grid[row][column] > 0:
                color = BLUE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Limit to 60 frames per second
    clock.tick(60)
    grid[ant1.x][ant1.y] -= 1
    ant1.move(N)
    grid[ant1.x][ant1.y] += 1

    for line in dead_ants:
        print(line)
    print('')

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
#pygame.quit()
