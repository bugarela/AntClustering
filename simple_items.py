from random import random, randint
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

N = 20
n_dead = 200
n_ants = 200
life = 75

MARGIN = 2
WIDTH = 800 / N - MARGIN
HEIGHT = 800 / N - MARGIN
#WINDOW_SIZE = [N * (WIDTH + MARGIN), N * (HEIGHT + MARGIN)]
WINDOW_SIZE = [800, 800]

vision_range = 2
dead_ants = []
grid = []

class Ant():
    def __init__(self, size):
        self.x = int(random() * size)
        self.y = int(random() * size)
        self.carrying = False
        self.life = life
        grid[self.x][self.y] += 1
    def move(self, size):
        if self.life == 0 and not self.carrying:
            grid[self.x][self.y] -= 1
        else:
            self.x = max(min(self.x + randint(-1,1), size-1), 0)
            self.y = max(min(self.y + randint(-1,1), size-1), 0)

            xmin = self.x-vision_range
            xmax = self.x+vision_range+1
            ymin = self.y-vision_range
            ymax = self.y+vision_range+1

            n_local = sum([sum(row[ymin : ymax]) for row in dead_ants[xmin : xmax]])
            field_size = (1 + 2*vision_range)**2 - 1
            if not self.carrying and dead_ants[self.x][self.y] == 1:
                p = 1.0*n_local / field_size
                if random() > p**2:
                    self.carrying = True
                    dead_ants[self.x][self.y] = 0
                    self.life = life
                else:
                    self.life-=1
            if self.carrying and dead_ants[self.x][self.y] == 0:
                p = (n_local + 0.1) / field_size
                if random() < p**2:
                    self.carrying = False
                    dead_ants[self.x][self.y] = 1
                    self.life = life
                else:
                    self.life-=1
            else:
                self.life-=1

def generate_grid(size=100):
    return [[0 for _ in range(size)] for _ in range(size)]

def spreads_items(grid, n_items):
    i = 0
    j = 0
    for _ in range(n_items):
        while(grid[i][j] != 0):
            i = int(random() * len(grid))
            j = int(random() * len(grid))
        grid[i][j] = 1
    return grid

grid = generate_grid(N)
ants = [Ant(N) for _ in range(n_ants)]
dead_ants = spreads_items(generate_grid(N), n_dead)

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Ant Clustering")
done = False
clock = pygame.time.Clock()

screen.fill(BLACK)

while(not done):
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

    clock.tick(60)
    for ant in ants:
        grid[ant.x][ant.y] -= 1
        ant.move(N)
        grid[ant.x][ant.y] += 1


    pygame.display.flip()

pygame.quit()
