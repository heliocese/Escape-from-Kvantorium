import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.delay = 100
        pygame.time.set_timer(30, self.delay)
        w, h = 19, 40
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color((0, 0, 123)))
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def get_position(self):
        return self.x, self.y

    def set_position(self, pos):
        self.x, self.y = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, pos):
        next_pos = pos
        self.set_position(next_pos)
