from random import random, randint
#from matplotlib import pyplot as plt
#from matplotlib import animation

class Ant():
    def __init__(self, size):
        self.x = int(random() * size)
        self.y = int(random() * size)
        self.state = 0
    def move(self):
        self.x += randint(-1,1)
        self.y += randint(-1,1)

vision_field = 8

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

test_grid = generate_grid(10)
filled_grid = spreads_itens(test_grid, 60)
for line in filled_grid:
    print(line)

while(1):
    ant1 = Ant(10)
    ant1.move()
    filled_grid[ant1.x][ant1.y] = 8
    for line in filled_grid:
        print(line)
