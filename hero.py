import pygame
import pyganim


COLOR = "#090909"
GRAVITY = 0.35
JUMP_POWER = 10
data = 'data/characters/animation/'


ANIMATION_DELAY = 50  # скорость смены кадров
ANIMATION_RIGHT = [(data + 'Alice_rr1.png'), (data + 'Alice_rr2.png'), (data + 'Alice_rr3.png'), (data + 'Alice_rr4.png')]
ANIMATION_LEFT = [(data + 'Alice_rl1.png'), (data + 'Alice_rl2.png'), (data + 'Alice_rl3.png'), (data + 'Alice_rl4.png')]
ANIMATION_JUMP_LEFT = [(data + 'Alice_rl1.png', 50)]
ANIMATION_JUMP_RIGHT = [(data + 'Alice_rr1.png', 50)]
ANIMATION = [(data + 'Alice_0.png', 50)]


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.image = pygame.Surface((16, 40))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, 16, 40)
        self.rect = self.image.get_rect(center=(x, y))
        self.image.set_colorkey((9, 9, 9))
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False

        self.image.set_colorkey(pygame.Color(COLOR))  # делаем фон прозрачным
        #        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:

            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRight.scale((16, 40))
        #        Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.scale((16, 40))
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION)
        self.boltAnimStay.play()
        self.boltAnimStay.scale((16, 40))
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.scale((16, 40))
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.scale((16, 40))
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION)
        self.boltAnimJump.scale((16, 40))
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

