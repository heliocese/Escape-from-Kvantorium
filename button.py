import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, second_image, text=None, scale=2):
        pygame.sprite.Sprite.__init__(self)
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
        self.is_text = False
        if text:
            self.is_text = True
            self.text = text
            font = pygame.font.Font(None, 36)
            self.text = font.render(self.text, True, (0, 0, 15))
            self.text_rect = self.text.get_rect(center=(x, y))

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


class CheckButton(Button):
    def __init__(self, x, y, unchecked_image, unchecked_image_, checked_image, checked_image_, is_checked=False,
                 scale=2):
        Button.__init__(self, x, y, checked_image, checked_image_, text=None, scale=4)
        pygame.sprite.Sprite.__init__(self)
        self.unchecked_image = pygame.transform.scale(unchecked_image, (int(unchecked_image.get_width() * scale),
                                                                        int(unchecked_image.get_height() * scale)))
        self.unchecked_image_ = pygame.transform.scale(unchecked_image_, (int(unchecked_image_.get_width() * scale),
                                                                          int(unchecked_image_.get_height() * scale)))
        self.checked_image = pygame.transform.scale(checked_image, (int(checked_image.get_width() * scale),
                                                                    int(checked_image.get_height() * scale)))
        self.checked_image_ = pygame.transform.scale(checked_image_, (int(checked_image_.get_width() * scale),
                                                                      int(checked_image_.get_height() * scale)))
        self.is_checked = is_checked
        if self.is_checked:
            self.cur_image = self.checked_image
        else:
            self.cur_image = self.unchecked_image
        self.rect = self.cur_image.get_rect(center=(x, y))

    def update(self, screen):
        screen.blit(self.cur_image, self.rect)

    def change_colour(self, pos):
        if self.rect.collidepoint(pos):
            if self.is_checked:
                self.cur_image = self.checked_image_
            else:
                self.cur_image = self.unchecked_image_
        else:
            if self.is_checked:
                self.cur_image = self.checked_image
            else:
                self.cur_image = self.unchecked_image

    def check(self):
        self.is_checked = True

    def uncheck(self):
        self.is_checked = False
