import pygame
import sys
import os
import random
import textwrap


# загрузка изображения и обрезка заднего плана
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


# группы спрайтов для вертикальных и горизонтальных барьеров
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


# объект летающий в главном меню
class Object(pygame.sprite.Sprite):
    def __init__(self, image, x, y, *groups):
        super().__init__(*groups)
        # изображение
        self.image = pygame.transform.scale(image,
                                            (int(image.get_width() * 2),
                                             int(image.get_height() * 2)))
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = random.randint(-5, 5)  # случайно заданное направление по оси x
        self.vy = random.randrange(-5, 5)  # случайно заданное направление по оси y

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)  # движение по направлению
        if pygame.sprite.spritecollideany(self, horizontal_borders):  # соприкосновение с горизонтальным барьером
            self.vy = -self.vy  # направление по оси y меняется на противоположное
        if pygame.sprite.spritecollideany(self, vertical_borders):  # соприкосновение с вертикальным барьером
            self.vx = -self.vx  # направление по оси x меняется на противоположное


# класс барьера для объектов
class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, *groups):
        super().__init__(*groups)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)  # добавление барьера в группу вертикальных
            self.image = pygame.Surface([1, y2 - y1])  # создание изображения
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)  # создание границ
        else:  # горизонтальная стенка
            self.add(horizontal_borders)  # добавление барьера в группу горизонтальных
            self.image = pygame.Surface([x2 - x1, 1])  # создание изображения
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)  # создание границ


# разбивка текста на несколько строк до определённой длины
def wrap(text, length):
    return textwrap.wrap(text, length)


# разбивка нескольких текстов на строки до определённой длины
def full_wrapper(text, length):
    new_text = []
    for string in text:  # проходимся по каждому строке текстов
        wrapped_string = wrap(string, length)  # оборачиваем строку
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


class Text(pygame.sprite.Sprite):
    def __init__(self, text, font, x, y, colour, *groups):
        super().__init__(*groups)
        self.image = font.render(text, True, colour)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, pos):
        self.rect = self.image.get_rect(center=pos)