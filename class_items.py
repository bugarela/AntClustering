from random import random, randint
import pygame
import pandas as pd
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 000, 255)
colors = [RED, GREEN, BLUE, PINK]

N = 50
n_dead = 200
n_ants = 200
life = 200
alpha = 40

MARGIN = 2
WIDTH = 600 / N - MARGIN
HEIGHT = 600 / N - MARGIN
WINDOW_SIZE = [600, 600]

vision_range = 2
dead_ants = []
alive_ants = []
items = []

class Ant():
    def __init__(self, size):
        self.x = int(random() * size)
        self.y = int(random() * size)
        self.carrying = False
        self.life = life
        alive_ants[self.x][self.y] += 1

    def move(self, size):
        if self.life == 0 and not self.carrying:
            alive_ants[self.x][self.y] -= 1
        else:
            self.x = max(min(self.x + randint(-1,1), size-1), 0)
            self.y = max(min(self.y + randint(-1,1), size-1), 0)

            xmin = self.x-vision_range
            xmax = self.x+vision_range+1
            ymin = self.y-vision_range
            ymax = self.y+vision_range+1

            foi = 0
            if dead_ants[self.x][self.y] != {}:
                for row in dead_ants[xmin : xmax]:
                    for item in row[ymin : ymax]:
                        if item != self and item != {}:
                            print(dead_ants[self.x][self.y], item)
                            foi += 1 - dissimilarity(dead_ants[self.x][self.y], item) / alpha

            field_size = (1 + 2*vision_range)**2 - 1
            if not self.carrying and dead_ants[self.x][self.y] == 1:
                p = (0.1 / (0.1 + foi))**2
                if random() < p:
                    self.carrying = True
                    dead_ants[self.x][self.y] = {}
                    self.life = life
                else:
                    self.life-=1
            if self.carrying and dead_ants[self.x][self.y] == {}:
                p = 2*foi
                if random() < p:
                    self.carrying = False
                    dead_ants[self.x][self.y] = self
                    self.life = life
                else:
                    self.life-=1
            else:
                self.life-=1

def generate_grid(size, fill):
    return [[fill for _ in range(size)] for _ in range(size)]

def spreads_itens(dead_ants, items):
    i = 0
    j = 0
    for item in items:
        while(dead_ants[i][j] != {}):
            i = int(random() * len(dead_ants))
            j = int(random() * len(dead_ants))
        dead_ants[i][j] = item
    return dead_ants

def dissimilarity(a, b):
    return np.sqrt((a['X']-b['X'])**2 + (a['Y']-b['Y'])**2)


df = pd.read_csv('input1.csv', names=['X', 'Y', 'Class'])
items = df.to_dict('index').values()

alive_ants = generate_grid(N, 0)
dead_ants = spreads_itens(generate_grid(N, {}), items)
ants = [Ant(N) for _ in range(n_ants)]

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
            if dead_ants[row][column] != {}:
                color = colors[dead_ants[row][column]['Class'] - 1]
            if alive_ants[row][column] > 0:
                color = WHITE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    clock.tick(60)
    for ant in ants:
        alive_ants[ant.x][ant.y] -= 1
        ant.move(N)
        alive_ants[ant.x][ant.y] += 1


    pygame.display.flip()

pygame.quit()
