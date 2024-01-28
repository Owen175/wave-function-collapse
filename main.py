import pygame

WIDTH = 16
HEIGHT = 16
TILE_DIMS = 56
# Choose the tile with the least entropy - the least number of tiles that could fit in that spot. If 0, backtrack,
# if more than 1, randomly select and log in a stack for backtracking
class Tile:
    def __init__(self, img, edges):
        # Each edge has 3 sockets which must match up to fit.
        self.img = img
        self.edges = edges

class Game:
    def __init__(self):
        tiles = self.load_tiles()
    def load_tiles(self):
        imgs = []
        for i in range(13):
            imgs.append(pygame.image.load(f'{i}.png'))
        ts = []