import pygame


COLOR = "#888888"
GRAVITY = 0.35
JUMP_POWER = 10


class Hero(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.image = pygame.Surface((22, 32))
        self.rect = pygame.Rect(x, y, 32, 22)  # прямоугольный объект
        self.image.set_colorkey(pygame.Color(COLOR))
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False

    def update(self):
            pass

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, left, right, up, platforms):
        if left:
            self.xvel = -5  # Лево = x- n

        if right:
            self.xvel = 5  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
        if not self.onGround:
            self.yvel += GRAVITY
            self.rect.y += self.yvel
            self.collide(0, self.yvel, platforms)
        if self.onGround:
            self.yvel = 0

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                print('fsdf')

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
        return self.rect.x + 20, self.rect.y + 20