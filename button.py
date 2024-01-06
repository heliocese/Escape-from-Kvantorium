import pygame


class Button:
    def __init__(self, x, y, image, second_image, text=None, scale=2):
        # super().__init__(all_sprites)
        # основное изображение
        self.image = pygame.transform.scale(image,
                                            (int(image.get_width() * scale),
                                             int(image.get_height() * scale)))
        # избражение используещееся при наведении на кнопку
        self.second_image = pygame.transform.scale(second_image,
                                                   (int(image.get_width() * scale),
                                                    int(image.get_height() * scale)))
        self.rect = self.image.get_rect(center=(x, y))
        self.cur_image = self.image
        # self.rect.topleft = (x, y)
        self.is_text = False
        if text:
            self.is_text = True
            self.text = text
            font = pygame.font.Font(None, 36)
            self.text = font.render(self.text, True, (0, 0, 15))
            self.text_rect = self.text.get_rect(center=(x, y))

    """def draw_text(self, screen):
        font = pygame.font.Font(None, 100)
        text = font.render(self.text, True, (0, 0, 0))
        screen.blit(text, self.rect)"""

    def update(self, screen):
        screen.blit(self.cur_image, self.rect)
        if self.is_text:
            screen.blit(self.text, self.text_rect)

    def click_check(self, pos):
        return self.rect.collidepoint(pos)

    def change_colour(self, pos):
        if self.rect.collidepoint(pos):
            self.cur_image = self.second_image
        else:
            self.cur_image = self.image

    """def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        #self.draw_text(screen)

        return action"""
