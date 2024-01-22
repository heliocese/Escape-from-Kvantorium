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
        self.name = Text(person, font, x + 10, y - 10, (20, 10, 30))  # рисовка имени персонажа над головой
        self.person = person   # имя персонажа
        self.w, self.h = 19, 40  # ширина и высота персонажа
        self.coords_list = []  # для получения последних координат, на которых был игрок, для уровня со спасением
        # другого персонажа
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.yvel = 0  # скорость вертикального перемещения
        self.xvel = 0  # скорость горизонтального перемещения
        self.onGround = False  # может ли падать игрок
        self.image.set_colorkey(pygame.Color(COLOR))  # делаем фон прозрачным
        self.delay, self.right, self.left, self.jump_right, self.jump_left, self.stay = get_animation(person)
        # для получения анимации персонажа
        self.stay.blit(self.image, (0, 0))  # По умолчанию, стоим

    def draw_name(self, screen, camera):  # рисуется имя над головой
        screen.blit(self.name, camera.apply(self.name))

    def draw(self, screen, camera):  # Выводим себя на экран
        screen.blit(self.image, camera.apply(self))
        # self.draw_name(screen, camera)

    def move(self, left, right, up, platforms, character):
        if left:  # если нажата клавиша для движения влево
            self.xvel = -5  # идем влево
            self.image.fill(pygame.Color(COLOR))
            if up:  # для прыжка влево есть отдельная анимация
                self.jump_left.blit(self.image, (0, 0))
            else:
                self.left.blit(self.image, (0, 0))

        if right:  # если нажата клавиша для движения вправо
            self.xvel = 5  # идем вправо
            self.image.fill(pygame.Color(COLOR))
            if up:  # отдельная анимация для прыжка
                self.jump_right.blit(self.image, (0, 0))
            else:
                self.right.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            self.image.fill(pygame.Color(COLOR))
            self.stay.blit(self.image, (0, 0))

        if up:  # если игрок прыгает
            if self.onGround:  # и находится на земле
                self.yvel = -JUMP_POWER * up  # прыгаем в зависимости от прыжка(простой, двойной)
        if not self.onGround:  # если игрок не на земле
            self.yvel += GRAVITY  # опускаем его
        self.rect.y += self.yvel  # переносим положение игрока
        self.collide(0, self.yvel, platforms, character)

        self.rect.x += self.xvel  # переносим положение игрока
        self.collide(self.xvel, 0, platforms, character)

        if isinstance(character, Students):  # если на уровне есть доп персонаж
            if character.flag:  # и до него уже добежал игрок
                character.image.fill(pygame.Color(COLOR))
                if self.get_position()[:2] not in self.coords_list:  # меняет положение на последние координаты игрока
                    self.coords_list.append(self.get_position()[:2])
                if left:  # делаем анимацию в зависимости от направления движения
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

    def get_position(self):  #получение координат персонажа
        return self.rect.x, self.rect.y, self.rect.right - self.rect.left,  self.rect.bottom - self.rect.top
