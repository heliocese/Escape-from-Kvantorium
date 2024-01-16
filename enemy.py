import pygame


class Teacher(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        w, h = 19, 40
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color((0, 0, 123)))
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def get_position(self):
        return self.x, self.y, 19, 40

    def set_position(self, pos):
        self.rect.center = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, pos):
        print(pos)
        next_pos = pos
        self.set_position(next_pos)


class Students(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        w, h = 19, 40
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color((0, 0, 123)))
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.flag = False

    def move(self, pos):
        if self.flag:
            pass