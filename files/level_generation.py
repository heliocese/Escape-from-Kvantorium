import pytmx
import pygame

maps = 'data/levels'


class Labirint:
    # a - айди клеток по которым можно ходить
    # b - айди клетки выхода
    def __init__(self, filename, a, b):
        self.map = pytmx.load_pygame(f'{maps}/{filename}')
        self.height = self.map.height  # высота
        self.width = self.map.width  # ширина
        self.tile_size = self.map.tilewidth
        self.free_tiles = a
        self.finish_tile = b
        self.platform = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        for i in range(2):  # генерируется уровень по слоям
            for y in range(self.height):
                for x in range(self.width):
                    image = self.map.get_tile_image(x, y, i)
                    if image:  # если есть тайл в клетке
                        sprite = Sprite(image, x, y, self.tile_size)  # то добавляем в группу спрайтов
                        self.sprites.add(sprite)
                        if self.map.tiledgidmap[self.map.get_tile_gid(x, y, i)] == 18:
                            self.platform.add(sprite)  # отслеживаюся спрайты, по которым игрок ходит

    def size(self):  # размер карты в блоках
        return self.height, self.width

    def render(self, screen):  # отрисовывается уровень
        self.sprites.draw(screen)

    def get_tile_id(self, pos):  # получаем id тайла по координатам
        try:
            x, y = pos[0] / self.tile_size, pos[1] / self.tile_size  # делим на размер клетки, тк у нас
            # масштабированная карта
            return self.map.tiledgidmap[self.map.get_tile_gid(x, y,0)]
        except Exception:
            return False

    def is_free(self, pos):  # получаем ответ куда можно ходить
        x1, x2 = pos[0], pos[0] + pos[2] - 1
        y = pos[1] + pos[3]
        if self.get_tile_id((x1, y)) in self.free_tiles and self.get_tile_id((x2, y)) in self.free_tiles:
            return True
        return False


class Sprite(pygame.sprite.Sprite):  # используем для блоков уровня(стены, пол)
    def __init__(self, image, x, y, size):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * size
        self.rect.y = y * size

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
