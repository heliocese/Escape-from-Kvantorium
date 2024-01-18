import pygame
from files.functions import load_image

# IMAGE = load_image('pictures/red_arrow.png', (255, 255, 255))
IMAGE = pygame.image.load('./data/pictures/red_arrow.png')
IMAGE.set_colorkey((255, 255, 255))


class Graffiti(pygame.sprite.Sprite):
    def __init__(self, coords, direction):
        super().__init__()
        self.image = IMAGE
        self.image_left = self.image
        self.image_down = pygame.transform.rotate(self.image_left, 90)
        self.image_right = pygame.transform.rotate(self.image_left, 180)
        self.image_up = pygame.transform.rotate(self.image_left, -90)
        self.change_direction(direction)
        self.rect = self.image.get_rect(center=coords)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, mouse_pos):
        self.rect = self.image.get_rect(center=mouse_pos)

    def change_direction(self, direction):
        self.image = self.image_right if direction == 'RIGHT' else self.image_left if direction == 'LEFT' \
            else self.image_up if direction == 'UP' else self.image_down
