import pygame


class Stars(pygame.sprite.Sprite):
    def __init__(self, active_image, position, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.active_image = pygame.transform.scale(active_image, (int(active_image.get_width() * 10),
                                                                  int(active_image.get_height() * 10)))
        self.image = self.active_image
        if position == 'middle':
            self.rect = self.image.get_rect(center=(x, y))
        elif position == 'left':
            self.rect = self.image.get_rect(center=(x - 170, y))
        elif position == 'right':
            self.rect = self.image.get_rect(center=(x + 170, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

