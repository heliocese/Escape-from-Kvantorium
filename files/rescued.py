import pygame

class Lost(pygame.sprite.Sprite):
    def __init__(self, coords, direction):
        super().__init__()
        self.image = IMAGE
        self.image_left = self.image
        self.image_down = pygame.transform.rotate(self.image_left, 90)
        self.image_right = pygame.transform.rotate(self.image_left, 180)
        self.image_up = pygame.transform.rotate(self.image_left, -90)
        self.change_direction(direction)
        self.rect = self.image.get_rect(center=coords)