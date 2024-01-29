import random
import pygame


# Choose the tile with the least entropy - the least number of tiles that could fit in that spot. If 0, backtrack,
# if more than 1, randomly select and log in a stack for backtracking
class Tile:
    def __init__(self, img: int, edges):
        # Each edge has 3 sockets which must match up to fit.
        self.img = img
        self.edges = edges


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH = 32
        self.HEIGHT = 16
        self.TILE_DIMS = 56
        self.screen = pygame.display.set_mode((self.WIDTH * self.TILE_DIMS, self.HEIGHT * self.TILE_DIMS))
        pygame.display.set_caption('Wave Function Collapse - Circuit')
        self.tiles = self.load_tiles()
        self.grid = [[None for _ in range(self.HEIGHT)] for _ in range(self.WIDTH)]
        self.num_tiles = len(self.tiles)
        self.entropy_grid = [[self.num_tiles for _ in range(self.HEIGHT)] for _ in range(self.WIDTH)]
        # Accessed as x, y
        self.stack = []
    def load_tiles(self):
        self.imgs = []
        for i in range(13):
            self.imgs.append(pygame.image.load(f'./images/circuit/{i}.png'))
        ts = []
        # 0 is black
        # 1 is green
        # 2 is turquoise
        # 3 is gray
        # Clockwise from the top
        ts.append(Tile(0, [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]))
        ts.append(Tile(1, [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]))
        ts.append(Tile(2, [[1, 1, 1], [1, 2, 1], [1, 1, 1], [1, 1, 1]]))
        ts.append(Tile(3, [[1, 1, 1], [1, 3, 1], [1, 1, 1], [1, 3, 1]]))
        ts.append(Tile(4, [[0, 1, 1], [1, 2, 1], [1, 1, 0], [0, 0, 0]]))
        ts.append(Tile(5, [[0, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 0]]))
        ts.append(Tile(6, [[1, 1, 1], [1, 2, 1], [1, 1, 1], [1, 2, 1]]))
        ts.append(Tile(7, [[1, 3, 1], [1, 2, 1], [1, 3, 1], [1, 2, 1]]))
        ts.append(Tile(8, [[1, 3, 1], [1, 1, 1], [1, 2, 1], [1, 1, 1]]))
        ts.append(Tile(9, [[1, 2, 1], [1, 2, 1], [1, 1, 1], [1, 2, 1]]))
        ts.append(Tile(10, [[1, 2, 1], [1, 2, 1], [1, 2, 1], [1, 2, 1]]))
        ts.append(Tile(11, [[1, 2, 1], [1, 2, 1], [1, 1, 1], [1, 1, 1]]))
        ts.append(Tile(12, [[1, 1, 1], [1, 2, 1], [1, 1, 1], [1, 2, 1]]))

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
        img, edges = self.imgs[tile.img], tile.edges

        new_img = pygame.transform.rotate(img, -90 * num)
        # Anticlockwise rotation of specified angle in degrees
        self.imgs.append(new_img)
        new_edges = [0, 0, 0, 0]

        for i, edge in enumerate(edges):
            new_edges[(i + num) % 4] = edge

        return Tile(len(self.imgs)-1, new_edges)

    def play(self):
        c = True
        while c:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    c = False
            (x, y), entropy = self.get_lowest_entropy()
            if entropy == 0:
                # If entropy is 0, this is where you need to backtrack
                popped = self.stack.pop()
                while len(popped) != 4:
                    tile, x, y = popped
                    self.remove_tile(x, y)
                    # Removes the tile from the grid and from the screen and reverses entropy changes
                    popped = self.stack.pop()
                tile, x, y, poss_tiles = popped
                self.remove_tile(x, y)

                if len(poss_tiles) == 1:
                    tile = poss_tiles[0]
                    self.stack.append([tile, x, y])
                else:
                    tile = random.choice(poss_tiles)
                    poss_tiles.remove(tile)
                    self.stack.append([tile, x, y, poss_tiles])

                self.grid[x][y] = tile

                # Randomly chooses from the possible tiles.
                self.screen.blit(self.imgs[tile.img], (x * self.TILE_DIMS, y * self.TILE_DIMS))
                pygame.display.update(pygame.Rect((x * self.TILE_DIMS, y * self.TILE_DIMS), (self.TILE_DIMS,
                                                                                             self.TILE_DIMS)))
                # Adds the tile to the screen.

                self.update_entropy(x, y)
            elif entropy == 37:
                c = False
            elif c:
                poss_tiles = self.get_possible_tiles(x, y)
                tile = random.choice(poss_tiles)
                if len(poss_tiles) == 1:
                    self.stack.append([tile, x, y])
                else:
                    poss_tiles.remove(tile)
                    self.stack.append([tile, x, y, poss_tiles])

                self.grid[x][y] = tile

                # Randomly chooses from the possible tiles.
                self.screen.blit(self.imgs[tile.img], (x * self.TILE_DIMS, y * self.TILE_DIMS))
                pygame.display.update(pygame.Rect((x * self.TILE_DIMS, y * self.TILE_DIMS), (self.TILE_DIMS,
                                                                                             self.TILE_DIMS)))
                # Adds the tile to the screen.

                self.update_entropy(x, y)
        input()

    def get_possible_tiles(self, x, y):
        left, right, up, down = -1, -1, -1, -1
        if y > 0:
            up = self.grid[x][y - 1]
        if y < self.HEIGHT - 1:
            down = self.grid[x][y + 1]
        if x > 0:
            left = self.grid[x - 1][y]
        if x < self.WIDTH - 1:
            right = self.grid[x + 1][y]
        # Gets the tiles surrounding it

        # Returns the tiles that can be placed there
        return [tile for tile in self.tiles if self.can_be_placed(tile, x, y, left, right, up, down)]

    def get_lowest_entropy(self):
        best = self.num_tiles + 1  # So the best must be changed
        coords = -1, -1
        for x, row in enumerate(self.entropy_grid):
            for y, entropy in enumerate(row):
                if entropy < best and entropy != -1:
                    best = entropy
                    coords = x, y

        return coords, best

    def update_entropy(self, x, y, removing=False):
        if not removing:
            self.entropy_grid[x][y] = -1

        up, down, left, right = 0, 0, 0, 0
        for t in self.tiles:
            if self.can_be_placed(t, x, y + 1):
                down += 1
            if self.can_be_placed(t, x, y - 1):
                up += 1
            if self.can_be_placed(t, x - 1, y):
                left += 1
            if self.can_be_placed(t, x + 1, y):
                right += 1
        # Gets the number of the tiles that can be placed in (x, y)

        if y > 0:
            if self.entropy_grid[x][y - 1] != -1:
                self.entropy_grid[x][y - 1] = up
        if y < self.HEIGHT - 1:
            if self.entropy_grid[x][y + 1] != -1:
                self.entropy_grid[x][y + 1] = down
        if x > 0:
            if self.entropy_grid[x - 1][y] != -1:
                self.entropy_grid[x - 1][y] = left
        if x < self.WIDTH - 1:
            if self.entropy_grid[x + 1][y] != -1:
                self.entropy_grid[x + 1][y] = right

    def can_be_placed(self, tile, x, y, left=-2, right=-2, up=-2, down=-2):
        if left == right == up == down == -2:  # Only if they need to be regenerated - to save time
            if y < 0 or x < 0 or y >= self.HEIGHT or x >= self.WIDTH:
                return True

            left, right, up, down = -1, -1, -1, -1
            if y > 0:
                up = self.grid[x][y - 1]
            if y < self.HEIGHT - 1:
                down = self.grid[x][y + 1]
            if x > 0:
                left = self.grid[x - 1][y]
            if x < self.WIDTH - 1:
                right = self.grid[x + 1][y]

        surrounding = [up, right, down, left]
        return [self.compare_sockets(tile, side, i) for i, side in enumerate(surrounding)] == [True] * 4

    def compare_sockets(self, tile, side, index):
        # Returns true if the sockets match, or if the side is off the screen or not yet assigned
        if side != -1 and side is not None:
            return tile.edges[index] == list(reversed(side.edges[(index + 2) % 4]))
            # Reversed as both edges go clockwise around the tile, so meet going opposite directions
        return True

    def remove_tile(self, x, y):
        self.grid[x][y] = None
        rectangle = pygame.Surface((self.TILE_DIMS, self.TILE_DIMS))
        rectangle.fill(pygame.Color(0, 0, 0))
        self.screen.blit(rectangle, (x * self.TILE_DIMS, y * self.TILE_DIMS))
        pygame.display.update()
        self.update_entropy(x, y, removing=True)
        self.entropy_grid[x][y] = 0
        for t in self.tiles:
            if self.can_be_placed(t, x, y):
                self.entropy_grid[x][y] += 1
                # Resets the entropy for x, y


g = Game()
g.play()