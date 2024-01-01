import pygame


COLOR = "#888888"
GRAVITY = 0.35
JUMP_POWER = 10


class Hero(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = pygame.Surface((22, 32))
        self.rect = pygame.Rect(x, y, 32, 22)  # прямоугольный объект
        self.image.set_colorkey(pygame.Color(COLOR))
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False

    def update(self):
            pass

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, left, right, up):
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

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel

        self.rect.x += self.xvel  # переносим свои положение на xvel

    def get_position(self):
        return self.x, self.y


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(self)
        #self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        #self.image.fill(Color(PLATFORM_COLOR))
        #self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)