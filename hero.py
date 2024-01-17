import pygame
from data_levels import get_animation


COLOR = "#090909"
GRAVITY = 0.35
JUMP_POWER = 10

vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный отрезок (стена для выхода)
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, person, reasons):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        w, h = 19, 40
        self.coords_list = []
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, w, h)
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False
        self.reasons = reasons
        self.image.set_colorkey(pygame.Color(COLOR))  # делаем фон прозрачным
        self.delay, self.right, self.left, self.jump_right, self.jump_left, self.stay = get_animation(person)
        self.stay.blit(self.image, (0, 0))  # По умолчанию, стоим

    def update(self):
        pass

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, left, right, up, platforms, character):
        if self.get_position()[:2] not in self.coords_list:
            self.coords_list.append(self.get_position()[:2])

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

        if character:
            character.image.fill(pygame.Color(COLOR))
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

    def exit(self):  # найден выход
        p = Border(959, 0, 959, 608)
        if self.reasons == 1:
            p = Border(1050, 0, 1050, 700)
        elif self.reasons == 3:
            p = Border(1812, 0, 1812, 1000)
        elif self.reasons == 4:
            p = Border(1710, -1000, 1710, 1000)
        elif self.reasons == 5:
            p = Border(2155, -1000, 2155, 5000)
        elif self.reasons == 6:
            p = Border(2103, -1000, 2103, 5000)
        elif self.reasons == 7:
            p = Border(2230, -1000, 2230, 5000)
        elif self.reasons == 8:
            p = Border(2530, -1000, 2530, 5000)
        elif self.reasons == 9:
            p = Border(2887, -1000, 2887, 5000)
        if pygame.sprite.collide_rect(self, p):
            return True
        return False

    def collide(self, xvel, yvel, platforms, character):
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
        if character:
            if pygame.sprite.collide_rect(self, character):
                character.flag = True

    def get_position(self):
        return self.rect.x, self.rect.y, self.rect.right - self.rect.left,  self.rect.bottom - self.rect.top
