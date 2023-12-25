import pygame
import sys
import os
from button import Button
from settings import *
from functions import load_image

pygame.init()  # инициализация pygame

pygame.display.set_caption('Проект')  # изменяем название окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # устанавливаем размеры экрана
icon = load_image('gogol.png')  # добавляем иконку окна
pygame.display.set_icon(icon)  # ставим нашу иконку вместо стандартной

clock = pygame.time.Clock()

bg_image = load_image('pattern4.png')
bg_image1 = load_image('pattern5.png')


def get_background(image):
    tiles = []
    width, height = image.get_width(), image.get_height()
    for i in range(WIDTH // width + 2):
        for j in range(HEIGHT // height + 2):
            tiles.append((i * width, j * height))
    return tiles


def draw_backgound(tiles, offset, image):
    print(offset)
    for tile in tiles:
        screen.blit(image, (tile[0] - offset, tile[1] - offset))


def terminate():
    pygame.quit()
    sys.exit()


def main_menu():  # главное меню
    text = 'Escape from Kvantorium'

    fon = pygame.transform.scale(load_image('bg1.jpg'), (WIDTH, HEIGHT))
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

    play_btn = Button(100, 100, play_img, 2.5)
    char_sel_btn = Button(100, 200, char_sel_img, 2.5)
    statistics_btn = Button(100, 300, statistics_img, 2.5)
    settings_btn = Button(100, 400, settings_img, 2.5)
    exit_btn = Button(100, 500, exit_img, 2.5)
    buttons = [play_btn, char_sel_btn, statistics_btn, settings_btn, exit_btn]

    # buttons_sprites = pygame.sprite.Group()
    tiles = get_background(bg_image)
    count = 0

    while True:

        ticks = pygame.time.get_ticks()
        if ticks % fps:
            count += 0.5

        draw_backgound(tiles, int(count % 32), bg_image)
        screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if play_btn.draw(screen):
            print('Играй')
            levels()
            break
        if char_sel_btn.draw(screen):
            print('Выбери персонажа')
        if statistics_btn.draw(screen):
            print('Смотри статистику')
        if settings_btn.draw(screen):
            print('Настрой себя')
        if exit_btn.draw(screen):
            terminate()

        pygame.display.flip()
        clock.tick(fps)


def levels():
    text = 'Выберите уровень'

    fon = pygame.transform.scale(load_image('bg.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 64)

    string_rendered = font.render(text, 1, (28, 28, 28))
    intro_rect = string_rendered.get_rect()
    text_coord = 10
    intro_rect.top = text_coord
    intro_rect.x = 40
    screen.blit(string_rendered, intro_rect)

    img_1 = load_image('1.png')
    return_img = load_image('return_btn.png')

    btn_1 = Button(150, 150, img_1, 2)
    return_btn = Button(25, 25, return_img, 1)

    # buttons_sprites = pygame.sprite.Group()

    tiles = get_background(bg_image1)
    print('ok')
    count = 0

    while True:

        ticks = pygame.time.get_ticks()
        if ticks % fps:
            count += 0.5

        draw_backgound(tiles, int(count % 32), bg_image1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if return_btn.draw(screen):
            main_menu()
            break
        if btn_1.draw(screen):
            print('level1')

        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main_menu()
