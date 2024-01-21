import pygame


class Star(pygame.sprite.Sprite):
    def __init__(self, active_image, inactive_image, position, button):
        pygame.sprite.Sprite.__init__(self)
        self.active_image = pygame.transform.scale(active_image, (int(active_image.get_width() * 2),
                                                                  int(active_image.get_height() * 2)))
        self.inactive_image = pygame.transform.scale(inactive_image, (int(inactive_image.get_width() * 2),
                                                                      int(inactive_image.get_height() * 2)))
        self.image = self.inactive_image
        if position == 'middle':
            self.rect = self.image.get_rect(center=(button.rect.x + button.image.get_width() * 0.5,
                                                    button.rect.y + button.image.get_height() * 1.15))
        elif position == 'left':
            self.rect = self.image.get_rect(center=(button.rect.x + button.image.get_width() * 0.3,
                                                    button.rect.y + button.image.get_height() * 1.2))
        elif position == 'right':
            self.rect = self.image.get_rect(center=(button.rect.x + button.image.get_width() * 0.7,
                                                    button.rect.y + button.image.get_height() * 1.2))

    def draw(self, screen):  # рисование звезд
        screen.blit(self.image, self.rect)

    def activate(self):  # желтая звезда
        self.image = self.active_image
