import pygame

# загружаем изображение
IMAGE = pygame.image.load('./data/pictures/red_arrow.png')
IMAGE.set_colorkey((255, 255, 255))  # делаем изображение прозрачным


# класс для создания граффити
class Graffiti(pygame.sprite.Sprite):
    def __init__(self, coords, direction):
        super().__init__()
        self.image = IMAGE  # берём изображение для стрелки
        self.image_left = self.image  # изначально стрелка направлена влево
        self.image_down = pygame.transform.rotate(self.image_left, 90)  # стрелка вниз
        self.image_right = pygame.transform.rotate(self.image_left, 180)  # стрелка вправо
        self.image_up = pygame.transform.rotate(self.image_left, -90)  # стрелка вверх
        self.change_direction(direction)
        self.rect = self.image.get_rect(center=coords)  # установка изначальных координат

    def draw(self, screen):  # отрисовка граффити
        screen.blit(self.image, self.rect)

    def update(self, pos):  # изменение координат граффити
        self.rect = self.image.get_rect(center=pos)

    def change_direction(self, direction):  # смена направленя, куда смотрит стрелка
        self.image = self.image_right if direction == 'RIGHT' else self.image_left if direction == 'LEFT' \
            else self.image_up if direction == 'UP' else self.image_down
