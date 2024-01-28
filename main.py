import pygame



# Choose the tile with the least entropy - the least number of tiles that could fit in that spot. If 0, backtrack,
# if more than 1, randomly select and log in a stack for backtracking
class Tile:
    def __init__(self, img, edges):
        # Each edge has 3 sockets which must match up to fit.
        self.img = img
        self.edges = edges


class Game:
    def __init__(self):
        self.WIDTH = 16
        self.HEIGHT = 16
        self.TILE_DIMS = 56
        self.screen = pygame.display.set_mode((self.WIDTH * self.TILE_DIMS, self.HEIGHT * self.TILE_DIMS))
        self.tiles = self.load_tiles()
        self.grid = [[None for _ in range(self.HEIGHT)] for _ in range(self.WIDTH)]
        # Accessed as x, y

    def load_tiles(self):
        imgs = []
        for i in range(13):
            imgs.append(pygame.image.load(f'./images/circuit/{i}.png'))
        ts = []
        # 0 is black
        # 1 is green
        # 2 is turquoise
        # 3 is gray
        # Clockwise from the top
        ts.append(Tile(imgs[0], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]))
        ts.append(Tile(imgs[1], [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]))
        ts.append(Tile(imgs[2], [[1, 1, 1], [1, 2, 1], [1, 1, 1], [1, 1, 1]]))
        ts.append(Tile(imgs[3], [[1, 1, 1], [1, 3, 1], [1, 1, 1], [1, 3, 1]]))
        ts.append(Tile(imgs[4], [[0, 1, 1], [1, 2, 1], [1, 1, 0], [0, 0, 0]]))
        ts.append(Tile(imgs[5], [[0, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 0]]))
        ts.append(Tile(imgs[6], [[1, 1, 1], [1, 2, 1], [1, 1, 1], [1, 2, 1]]))
        ts.append(Tile(imgs[7], [[1, 3, 1], [1, 2, 1], [1, 3, 1], [1, 2, 1]]))
        ts.append(Tile(imgs[8], [[1, 3, 1], [1, 1, 1], [1, 2, 1], [1, 1, 1]]))
        ts.append(Tile(imgs[9], [[1, 2, 1], [1, 2, 1], [1, 1, 1], [1, 2, 1]]))
        ts.append(Tile(imgs[10], [[1, 2, 1], [1, 2, 1], [1, 2, 1], [1, 2, 1]]))
        ts.append(Tile(imgs[11], [[1, 2, 1], [1, 2, 1], [1, 1, 1], [1, 1, 1]]))
        ts.append(Tile(imgs[12], [[1, 1, 1], [1, 2, 1], [1, 1, 1], [1, 2, 1]]))

        # Now rotating the tiles that need to be
        ts.append(self.copy_and_rotate(ts[2], 1))
        ts.append(self.copy_and_rotate(ts[2], 2))
        ts.append(self.copy_and_rotate(ts[2], 3))
        ts.append(self.copy_and_rotate(ts[3], 1))
        ts.append(self.copy_and_rotate(ts[4], 1))
        ts.append(self.copy_and_rotate(ts[4], 2))
        ts.append(self.copy_and_rotate(ts[4], 3))
        ts.append(self.copy_and_rotate(ts[5], 1))
        ts.append(self.copy_and_rotate(ts[5], 2))
        ts.append(self.copy_and_rotate(ts[5], 3))
        ts.append(self.copy_and_rotate(ts[6], 1))
        ts.append(self.copy_and_rotate(ts[7], 1))
        ts.append(self.copy_and_rotate(ts[8], 1))
        ts.append(self.copy_and_rotate(ts[8], 2))
        ts.append(self.copy_and_rotate(ts[8], 3))
        ts.append(self.copy_and_rotate(ts[9], 1))
        ts.append(self.copy_and_rotate(ts[9], 2))
        ts.append(self.copy_and_rotate(ts[9], 3))
        ts.append(self.copy_and_rotate(ts[10], 1))
        ts.append(self.copy_and_rotate(ts[11], 1))
        ts.append(self.copy_and_rotate(ts[11], 2))
        ts.append(self.copy_and_rotate(ts[11], 3))
        ts.append(self.copy_and_rotate(ts[12], 1))

        return ts
    def copy_and_rotate(self, tile, num):
        img, edges = tile.img, tile.edges
        self.screen.blit(img, (0,0))
        pygame.display.update()
        new_img = pygame.transform.rotate(img, -90 * num)
        new_edges = [0, 0, 0, 0]
        self.screen.blit(new_img, (0,0))
        pygame.display.update()
        for i, edge in enumerate(edges):
            new_edges[(i + num) % 4] = edge
        return Tile(new_img, new_edges)

    def play(self):
        pass
g = Game()






