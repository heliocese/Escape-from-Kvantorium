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
        del a[17]
        self.free_tiles = a
        self.finish_tile = b
        self.platform = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        platform = self.map.get_tile_image_by_gid(18)
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                sprite = Sprite(image, x, y, self.tile_size)
                self.sprites.add(sprite)
                if image == platform:
                    self.platform.add(sprite)

    def render(self, screen):
        self.sprites.draw(screen)

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(pos[0] / self.tile_size, pos[1] / self.tile_size, 0)]

    def is_free(self, pos):
        return self.get_tile_id(pos) in self.free_tiles


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, size):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * size
        self.rect.y = y * size

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
