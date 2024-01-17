import pygame
from data_levels import get_animation


COLOR = '#090909'

vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный отрезок (стена для выхода)
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)


class Teacher(pygame.sprite.Sprite):
    def __init__(self, x, y, person):
        super().__init__()
        pygame.time.set_timer(30, 100)
        self.x, self.y = x, y
        w, h = 19, 40
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color((0, 0, 123)))
        self.rect = pygame.Rect(x, y, w, h)
        self.image.set_colorkey((9, 9, 9))

    def get_position(self):
        return self.x, self.y, 19, 40

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, pos):
        self.rect.center = pos


class Students(pygame.sprite.Sprite):
    def __init__(self, x, y, person):
        super().__init__()
        self.x, self.y = x, y
        w, h = 19, 40
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, w, h)
        self.image.set_colorkey(pygame.Color(COLOR))
        self.flag = False
        self.reasons = '0'
        self.delay, self.right, self.left, self.jump_right, self.jump_left, self.stay = get_animation(person)
        #        Анимация движения вправо
        self.stay.blit(self.image, (0, 0))  # По-умолчанию, стоим

    def exit(self, reasons):  # найден выход
        self.reasons = int(reasons)
        p = Border(957, 0, 957, 608)
        if self.reasons == 1:
            p = Border(1048, 0, 1048, 700)
        elif self.reasons == 3:
            p = Border(1810, 0, 1810, 1000)
        elif self.reasons == 4:
            p = Border(1701, -1000, 1701, 1000)
        elif self.reasons == 5:
            p = Border(2153, -1000, 2153, 5000)
        elif self.reasons == 6:
            p = Border(2101, -1000, 2101, 5000)
        elif self.reasons == 7:
            p = Border(2227, -1000, 2227, 5000)
        elif self.reasons == 8:
            p = Border(2527, -1000, 2527, 5000)
        elif self.reasons == 9:
            p = Border(2885, -1000, 2885, 5000)
        if pygame.sprite.collide_rect(self, p):
            return True
        return False

    def move(self, coods_list, difference):
        if difference != 0:
            self.difference = difference
        if self.flag and len(coods_list) > 1:
            self.rect.x, self.rect.y = coods_list[-1][0] - self.difference, coods_list[-1][1]
            del coods_list[-1]

    def get_position(self):
        return self.rect.x, self.rect.y, self.rect.right - self.rect.left, self.rect.bottom - self.rect.top