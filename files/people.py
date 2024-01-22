import pygame
from files.data_levels import get_animation
from files.functions import Border


COLOR = '#090909'


class Teacher(pygame.sprite.Sprite):  # класс учителя для последнего уровня
    def __init__(self, x, y):
        super().__init__()
        self.person = 'Иван Дмитриевич'
        _, self.right, self.left, _, _, self.stay = get_animation('Иван Дмитриевич', (21, 43))
        # получение анимации
        w, h = 21, 43
        self.speed = 4  # скорость передвижения
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, w, h)
        self.image.set_colorkey((9, 9, 9))
        self.stay.blit(self.image, (0, 0))  # изначально стоит

    def get_position(self):  # получение координат
        return self.rect.x, self.rect.y, 19, 40

    def move(self, labirint):
        self.image.fill(pygame.Color(COLOR))   # обновляем анимацию
        if self.speed > 0:  # если бежит вправо
            self.right.blit(self.image, (0, 0))  # ставим анимацию движения вправо
            if (labirint.get_tile_id((self.rect.x + 32, self.rect.y - 16)) not in labirint.free_tiles or
                    labirint.get_tile_id((self.rect.x, self.rect.y + 50)) in labirint.free_tiles):
                # если учитель упирается в стенку или платформа заканчивается, то разворачивается
                self.speed *= -1
        elif self.speed < 0:  # если бежит влево
            self.left.blit(self.image, (0, 0))
            if (labirint.get_tile_id((self.rect.x, self.rect.y - 16)) not in labirint.free_tiles or
                    labirint.get_tile_id((self.rect.x, self.rect.y + 50)) in labirint.free_tiles):
                # если учитель упирается в стенку или платформа заканчивается, то разворачивается
                self.speed *= -1
        self.rect.x += self.speed


class Students(pygame.sprite.Sprite):  # класс доп персонажа, которого игрок спасает
    def __init__(self, x, y, person):
        super().__init__()
        self.person = person  # имя персонажа
        self.difference = None  # расстояние, на которое персонаж будет отставать отставать от игрока
        self.w, self.h = 19, 40  # высота и ширина
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.image.set_colorkey(pygame.Color(COLOR))
        self.flag = False  # бежит ли за игроком
        self.reasons = '0'
        self.delay, self.right, self.left, self.jump_right, self.jump_left, self.stay = get_animation(person)
        # получение анимации персонажа
        self.stay.blit(self.image, (0, 0))  # По умолчанию, стоим

    def exit(self, h, w):  # найден выход персонажем
        h = h * 32  # высота уровня
        w = w * 32 - 2  # ширина уровня
        p = Border(w, 0, w, h)
        if pygame.sprite.collide_rect(self, p):
            return True
        return False

    def move(self, coods_list, difference):  # двигаемся
        if difference != 0:  # записываем последнее направление, куда двигался игрок
            self.difference = difference
        if self.flag and len(coods_list) > 1:  # если игрок добежал до персонажа и в списке есть координаты
            self.rect.x, self.rect.y = coods_list[-1][0] - self.difference, coods_list[-1][1]
            # передвигается
            del coods_list[-1]  # удаляются последние координаты игрока

    def get_position(self):  # получение координат персонажа
        return self.rect.x, self.rect.y, self.w, self.h
