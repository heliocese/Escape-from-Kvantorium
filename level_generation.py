import pytmx
import pygame

maps = 'data/levels'


class Labirint:
    # a - айди клеток по которым можно ходить
    # b - айди клетки выхода
    def __init__(self, filename, a, b):
        self.map = pytmx.load_pygame(f'{maps}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = a
        self.finish_tile = b
        self.platform = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        for i in range(2):  # слои
            for y in range(self.height):
                for x in range(self.width):
                    image = self.map.get_tile_image(x, y, i)
                    if image:
                        sprite = Sprite(image, x, y, self.tile_size)
                        self.sprites.add(sprite)
                        if self.map.tiledgidmap[self.map.get_tile_gid(x, y, i)] == 18:
                            self.platform.add(sprite)

    def render(self, screen):
        self.sprites.draw(screen)

    def get_tile_id(self, pos):
        try:
            return self.map.tiledgidmap[self.map.get_tile_gid(pos[0] / self.tile_size, pos[1] / self.tile_size,0)]
        except Exception:
            return False

    def is_free(self, pos):
        x1, x2 = pos[0], pos[0] + pos[2] - 1
        y = pos[1] + pos[3]
        if self.get_tile_id((x1, y)) in self.free_tiles and self.get_tile_id((x2, y)) in self.free_tiles:
            return True
        return False

    """def find_path_step(self, start, target):
        INF = 1000
        start, target = (start[0] // 32, start[1] // 32), (target[0] // 32, target[1] // 32)
        x, y = start
        distance = [[INF] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        previous = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x * 32 < self.width * 32 and 0 <= next_y * 32 < self.height * 32 and \
                    self.is_free((next_x * 32 + 5, next_y * 32 + 5, 19, 40)) and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    previous[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return start[0] * 32, start[1] * 32
        while previous[y][x] != start:
            if previous[y][x]:
                x, y = previous[y][x]
        return x * 32, y * 32"""


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, size):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * size
        self.rect.y = y * size

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
