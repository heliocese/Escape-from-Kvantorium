import pygame
from files.data_levels import get_animation
from files.functions import Border


COLOR = '#090909'


class Teacher(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.delay, self.right, self.left, self.jump_right, self.jump_left, self.stay = get_animation('Иван Дмитриевич')
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
        self.person = person
        self.x, self.y = x, y
        w, h = 19, 40
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, w, h)
        self.image.set_colorkey(pygame.Color(COLOR))
        self.flag = False
        self.reasons = '0'
        self.delay, self.right, self.left, self.jump_right, self.jump_left, self.stay = get_animation(person)
        self.stay.blit(self.image, (0, 0))  # По умолчанию, стоим

    def exit(self, h, w):  # найден выход персонажем
        h = h * 32
        w = w * 32 - 2
        p = Border(w, 0, w, h)
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
