import pygame
from settings import *
from functions import *
# from button import Button

pygame.init()  # инициализация pygame

pygame.display.set_caption('Проект')  # изменяем название окна
screen = pygame.display.set_mode((width, height))  # устанавливаем размеры экрана
icon = load_image('gogol.png')  # добавляем иконку окна
pygame.display.set_icon(icon)  # ставим нашу иконку вместо стандартной

clock = pygame.time.Clock()


class Button:
    def __init__(self, x, y, image, scale=2):
        # super().__init__(all_sprites)
        image_width = image.get_width()
        image_height = image.get_height()
        self.image = pygame.transform.scale(image, (int(image_width * scale), int(image_height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                print('clicked')

        screen.blit(self.image, (self.rect.x, self.rect.y))


def terminate():
    pygame.quit()
    sys.exit()


def main_menu():  # главное меню
    text = 'Escape from Kvantorium'

    fon = pygame.transform.scale(load_image('bg1.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 64)

    string_rendered = font.render(text, 1, (28, 28, 28))
    intro_rect = string_rendered.get_rect()
    text_coord = 10
    intro_rect.top = text_coord
    intro_rect.x = 40
    screen.blit(string_rendered, intro_rect)

    play_img = load_image('play_btn.png')
    char_sel_img = load_image('character_select_btn.png')
    statistics_img = load_image('statistics_btn.png')
    settings_img = load_image('settings_btn.png')
    exit_img = load_image('exit_btn.png')

    play_btn = Button(100, 100, play_img)
    char_sel_btn = Button(100, 175, char_sel_img)
    statistics_btn = Button(100, 225, statistics_img)
    settings_btn = Button(100, 300, settings_img)
    exit_btn = Button(100, 375, exit_img)

    # buttons_sprites = pygame.sprite.Group()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        play_btn.draw()
        char_sel_btn.draw()
        statistics_btn.draw()
        settings_btn.draw()
        exit_btn.draw()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main_menu()
