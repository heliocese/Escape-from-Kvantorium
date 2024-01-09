import pygame
import pyganim
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
    def __init__(self, x, y, person):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        w, h = 19, 40
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, w, h)
        self.rect = self.image.get_rect(center=(x, y))
        self.image.set_colorkey((9, 9, 9))
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False

        self.image.set_colorkey(pygame.Color(COLOR))  # делаем фон прозрачным
        delay, right, left, jump_right, jump_left, stay = get_animation(person)
        #        Анимация движения вправо
        boltAnim = []
        for anim in right:

            boltAnim.append((anim, delay))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.scale((w, h))
        self.boltAnimRight.play()
        #        Анимация движения влево
        boltAnim = []
        for anim in left:
            boltAnim.append((anim, delay))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.scale((w, h))
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(stay)
        self.boltAnimStay.play()
        self.boltAnimStay.scale((w, h))
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(jump_left)
        self.boltAnimJumpLeft.scale((w, h))
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(jump_right)
        self.boltAnimJumpRight.scale((w, h))
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(stay)
        self.boltAnimJump.scale((w, h))
        self.boltAnimJump.play()

    def update(self):
            pass

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, left, right, up, platforms):
        if left:
            self.xvel = -5  # Лево = x- n
            self.image.fill(pygame.Color(COLOR))
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = 5  # Право = x + n
            self.image.fill(pygame.Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            self.image.fill(pygame.Color(COLOR))
            self.boltAnimStay.blit(self.image, (0, 0))

        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER * up
                self.image.fill(pygame.Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))
        if not self.onGround:
            self.yvel += GRAVITY
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def exit(self):  # найден выход
        p = Border(959, 0, 959, 608)
        if pygame.sprite.collide_rect(self, p):
            return True
        return False

    def collide(self, xvel, yvel, platforms):
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


    def get_position(self):
        return self.rect.x, self.rect.y, self.rect.right - self.rect.left,  self.rect.bottom - self.rect.top

