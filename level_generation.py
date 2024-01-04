import pytmx

maps = 'data/levels'


class Labirint:
    # a - айди клеток по которым можно ходить
    # b - айди клетки выхода
    def __init__(self, filename, a, b):
        self.map = pytmx.load_pygame(f'{maps}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        del a[17]
        self.free_tiles = a
        self.finish_tile = b

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                if image:
                    screen.blit(image, (x * self.tile_size, y * self.tile_size))
                image = self.map.get_tile_image(x, y, 1)
                if image:
                    screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(pos[0] / self.tile_size, pos[1] / self.tile_size, 0)]

    def is_free(self, pos):
        return self.get_tile_id(pos) in self.free_tiles
