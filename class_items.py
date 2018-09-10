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

values = [0, 255, 128]
colors = []
for r in values:
    for g in values:
        for b in values:
            colors.append((r, g, b))

colors = colors[1:-2]

'''
Primeiro grupo:
N = 30
n_ants = 80
alpha = 35
sigma = 2
life = 200
'''

N = 50
n_ants = 150
alpha = 1.3
sigma = 2
life = 200

MARGIN = 2
WIDTH = 600 / N - MARGIN
HEIGHT = 600 / N - MARGIN
WINDOW_SIZE = [600, 600]

vision_range = 1
dead_ants = []
alive_ants = []
items = []

class Ant():
    def __init__(self, size):
        self.x = int(random() * size)
        self.y = int(random() * size)
        self.carrying = {}
        self.life = life
        alive_ants[self.x][self.y] += 1

    def move(self, size):
        if self.life <= 0 and self.carrying == {}:
            alive_ants[self.x][self.y] -= 1
        else:
            self.x = max(min(self.x + randint(-1,1), size-1), 0)
            self.y = max(min(self.y + randint(-1,1), size-1), 0)

            xmin = self.x-vision_range
            xmax = self.x+vision_range+1
            ymin = self.y-vision_range
            ymax = self.y+vision_range+1

            foi = 0
            field_size = (1 + 2*vision_range)**2


            if self.carrying == {} and dead_ants[self.x][self.y] != {}:
                for row in dead_ants[xmin : xmax]:
                    for item in row[ymin : ymax]:
                        if item != dead_ants[self.x][self.y] and item != {}:
                            foi += max(1 - dissimilarity(dead_ants[self.x][self.y], item) / float(alpha), 0)

                foi = foi / float(sigma**2)


                if foi <= 1:
                    p = 1
                else:
                    p = 1 / float(foi**2)

                #if random () < 0.0005:
                print("Pegar: " + str(p))

                if random() < p:
                    self.carrying = dead_ants[self.x][self.y]
                    dead_ants[self.x][self.y] = {}
                    self.life = life
                else:
                    self.life-=1

            elif self.carrying != {} and dead_ants[self.x][self.y] == {}:
                for row in dead_ants[xmin : xmax]:
                    for item in row[ymin : ymax]:
                        if item != dead_ants[self.x][self.y] and item != {}:
                                foi += max(1 - dissimilarity(self.carrying, item) / float(alpha), 0)

                foi = foi / float(sigma**2)

                if foi >= 1:
                    p = 1
                else:
                    p = foi**4

                #if random () < 0.0005:
                print("Soltar: " + str(p))

                if random() < p:
                    dead_ants[self.x][self.y] = self.carrying
                    self.carrying = {}
                    self.life = life
                    #print("Dropou com foi =" + str(foi))
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


df = pd.read_csv('input2.tsv', sep='\t', names=['X', 'Y', 'Class'])
print(df.head())
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

    clock.tick(120)
    for ant in ants:
        alive_ants[ant.x][ant.y] -= 1
        ant.move(N)
        alive_ants[ant.x][ant.y] += 1


    pygame.display.flip()

pygame.quit()
