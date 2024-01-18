import pygame
import sys
import os
import random
import textwrap


def load_image(name, colorkey=None):
    fullname = os.path.join('./data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Object(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(image,
                                            (int(image.get_width() * 2),
                                             int(image.get_height() * 2)))
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)
        self.count = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def wrap(text, length):
    return textwrap.wrap(text, length)


def full_wrapper(text, length):
    new_text = []
    for string in text:
        wrapped_string = wrap(string, length)
        if len(wrapped_string) > 1:
            if text.index(string) < len(text) - 1:
                text[text.index(string) + 1] = ''.join(wrapped_string[1:]) + ' ' + text[text.index(string) + 1]
                new_text.append(wrapped_string[0])
            else:
                for sting_part in wrapped_string:
                    new_text.append(sting_part)
        else:
            new_text.append(string)
    return new_text
