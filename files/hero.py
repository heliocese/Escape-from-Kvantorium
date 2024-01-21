import pygame
from files.data_levels import get_animation
from files.people import Students
from files.functions import Text


COLOR = "#090909"
GRAVITY = 0.35
JUMP_POWER = 10

vertical_borders = pygame.sprite.Group()


# класс барьера
class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, *groups):
        super().__init__(*groups)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, person, font):
        pygame.sprite.Sprite.__init__(self)
        self.name = Text(person, font, x + 10, y - 10, (20, 10, 30))
        self.person = person
        self.xvel = 0
        self.w, self.h = 19, 40
        self.coords_list = []
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False
        self.image.set_colorkey(pygame.Color(COLOR))  # делаем фон прозрачным
        self.delay, self.right, self.left, self.jump_right, self.jump_left, self.stay = get_animation(person)
        self.stay.blit(self.image, (0, 0))  # По умолчанию, стоим

    def draw_name(self, screen, camera):
        screen.blit(self.name, camera.apply(self.name))

    def update(self):
        pass

    def draw(self, screen, camera):  # Выводим себя на экран
        screen.blit(self.image, camera.apply(self))
        # self.draw_name(screen, camera)

    def move(self, left, right, up, platforms, character):
        if left:
            self.xvel = -5  # Лево
            self.image.fill(pygame.Color(COLOR))
            if up:  # для прыжка влево есть отдельная анимация
                self.jump_left.blit(self.image, (0, 0))
            else:
                self.left.blit(self.image, (0, 0))

        if right:
            self.xvel = 5  # Право
            self.image.fill(pygame.Color(COLOR))
            if up:
                self.jump_right.blit(self.image, (0, 0))
            else:
                self.right.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            self.image.fill(pygame.Color(COLOR))
            self.stay.blit(self.image, (0, 0))

        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER * up
        if not self.onGround:
            self.yvel += GRAVITY
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, character)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms, character)

        if isinstance(character, Students):
            if character.flag:
                character.image.fill(pygame.Color(COLOR))
                if self.get_position()[:2] not in self.coords_list:
                    self.coords_list.append(self.get_position()[:2])
                if left:
                    if up:
                        character.jump_left.blit(character.image, (0, 0))
                    else:
                        character.left.blit(character.image, (0, 0))
                if right:
                    if up:
                        character.jump_right.blit(character.image, (0, 0))
                    else:
                        character.right.blit(character.image, (0, 0))
                if not(right or left):
                    character.stay.blit(character.image, (0, 0))

    def exit(self, h, w, prmt=True):  # найден выход персонажем
        h *= 32  # высота всей карты
        w *= 32  # ширина всей карты
        p = Border(w, 0, w, h)  # бордюр для выхода
        if pygame.sprite.collide_rect(self, p):
            self.rect.right = p.rect.left
            if prmt:  # запрет на выход без персонажа в уровнях спасения
                return True
        return False

    def collide(self, xvel, yvel, platforms, character):
        a = Border(0, -1000, 0, 5000)  # стена слева у входа
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает
        if isinstance(character, Students):
            if pygame.sprite.collide_rect(self, character):
                character.flag = True
        if pygame.sprite.collide_rect(self, a):  # запрет на выход из карты через вход
            self.rect.left = a.rect.right

    def get_position(self):
        return self.rect.x, self.rect.y, self.rect.right - self.rect.left,  self.rect.bottom - self.rect.top
