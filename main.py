import random

import pygame
import sys
import os
from button import Button
from settings import *
from functions import load_image, Object, Border, all_sprites, vertical_borders, horizontal_borders, wrap, full_wrapper
from level_generation import Labirint
from hero import Hero
from star import Star

pygame.init()  # инициализация pygame

pygame.display.set_caption('Проект')  # изменяем название окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # устанавливаем размеры экрана
icon = load_image('gogol.png')  # добавляем иконку окна
pygame.display.set_icon(icon)  # ставим нашу иконку вместо стандартной

clock = pygame.time.Clock()

main_font = pygame.font.Font(None, 64)

bg_image = load_image('pattern6.png')
bg_image1 = load_image('pattern13.png')
bg_image_character = load_image('pattern9.png')
# bg_images = [load_image('pattern9'), load_image('pattern10'),load_image('pattern11'), load_image('pattern12')]


def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((0, 0, 0))

    return image


person_sheet = load_image('levels/characters/Никита.png', (64, 60, 147))
person_image = get_image(person_sheet, 1, 48, 96, 4)

students = {
    'Никита': 'Успевает делать все задания в Лицее. Как именно это ему это удаётся никто не знает. Возможно освоил '
              'знания тайм менеджмента, ну, или же не спит ночами',
    'Ангелина': 'На втором занятии уже всех знала по именам. Коммуникабельная, в общем.  Однажды смогла договориться '
                'с муравьями, правда, не понятно, что больше помогло в переговорах: дихлофос или ее красноречие',
    'Коля': '',
    'Настя': '',
    'Алиса': '',
    'Ярик': '',
    'Саша': 'Умудрился вылететь из Яндекс лицея до первого дедлайна',
    'Влад': 'Ушел с лицея со словами "Чего-то у меня не получается с python, буду учить java"',
    'Ваня': 'На начало второго года знал как зовут Ангелину, Сашу и Никиту. Не смог пройти первый бонусный уровень с '
            'проектом, больше в Кванториуме его никто не видел. (разработчики сделали ему выпрямление, не удивляйтесь) '
}

button_image = load_image('button1.png')
button_image1 = load_image('button2.png')

button_list = ['Играть', 'Выбор персонажа', 'Статистика', 'Настройки', 'Выход']
main_menu_buttons = {}
for i in range(5):
    main_menu_buttons[button_list[i]] = Button(WIDTH // 2, HEIGHT // 7 * (i + 2),
                                               button_image, button_image1, button_list[i], 4)

return_img = load_image('return_btn.png')
return_img_ = load_image('return_btn_.png')

return_btn = Button(50, 50, return_img, return_img_)
level_btns = []

for i in range(1, 11):
    level_btns.append(Button(WIDTH // 6 * 5 if (i % 5) == 0 else WIDTH // 6 * (i % 5),
                             HEIGHT // 3 if i < 6 else HEIGHT // 3 * 2,
                             load_image(f'{i}.png'),
                             load_image(f'{i}_.png'), None, WIDTH // 240))

star_active = load_image('star_active.png')
star_inactive = load_image('star_inactive.png')

stars = []
for button in level_btns:
    stars.append([Star(star_active, star_inactive, 'left', button),
                 Star(star_active, star_inactive, 'right', button),
                  Star(star_active, star_inactive, 'middle', button)])


# заставки к уровням
def intro_maker(message, colour=(255, 255, 255)):  # пока убого работает
    messages = full_wrapper(message, WIDTH // 16)
    print(messages)
    cur_message = 0
    message_offsets = [50 * i for i in range(len(messages))]
    print(message_offsets)
    alpha, direction = 0, 2
    font = pygame.font.Font(None, 32)
    count, speed = 0, 3
    skip_text = font.render('Нажмите ЛЮБУЮ клавишу, чтобы продолжить', True, (255, 255, 255))
    skip_text.set_alpha(alpha)
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру

        for message in messages[0:cur_message]:
            string = font.render(message, True, colour)
            string_rect = string.get_rect(center=(WIDTH // 2, HEIGHT // 2 + message_offsets[messages.index(message)]))
            screen.blit(string, string_rect)

        if count < len(messages[cur_message]) * speed:
            count += 1
        elif cur_message < len(messages) - 1:
            count = 0
            cur_message += 1
            for i in range(len(message_offsets)):
                message_offsets[i] -= 25
            print(message_offsets)

        text = font.render(messages[cur_message][0:count // speed], True, colour)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + message_offsets[cur_message]))

        screen.blit(text, text_rect)

        alpha += direction

        if alpha == 0:
            direction = 2
        elif alpha == 100:
            direction = -2

        skip_text.set_alpha(alpha)

        screen.blit(skip_text, skip_text.get_rect(center=(WIDTH // 2, HEIGHT * 0.8)))

        pygame.display.flip()
        clock.tick(FPS)


def get_background(image):
    tiles = []
    width, height = image.get_width(), image.get_height()
    for i in range(WIDTH // width + 2):
        for j in range(HEIGHT // height + 2):
            tiles.append((i * width, j * height))
    return tiles


def draw_backgound(tiles, offset, image):
    # print(offset)
    for tile in tiles:
        screen.blit(image, (tile[0] - offset, tile[1] - offset))


def terminate():
    pygame.quit()
    sys.exit()


def main_menu():  # главное меню
    pygame.display.set_caption('Escape from Kvantorium')

    text = 'Escape from Kvantorium'

    fon = pygame.transform.scale(load_image('bg1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 64)

    string_rendered = font.render(text, 1, (28, 28, 28))
    text_rect = string_rendered.get_rect(center=(WIDTH // 2, HEIGHT // 10))
    screen.blit(string_rendered, text_rect)
    offscreen = 200

    Border(-offscreen, -offscreen, WIDTH + offscreen, -offscreen)  # - верхний
    Border(-offscreen, HEIGHT + offscreen, WIDTH + offscreen, HEIGHT + offscreen)  # - нижний
    Border(-offscreen, -offscreen, -offscreen, HEIGHT + offscreen)  # | левый
    Border(WIDTH + offscreen, -offscreen, WIDTH + offscreen, HEIGHT + offscreen)  # | правый

    coords_x = [i for i in range(-100, -50)] + [j for j in range(WIDTH + 50, WIDTH + 100)]
    coords_y = [i for i in range(-100, -50)] + [j for j in range(HEIGHT + 50, HEIGHT + 100)]
    objects = [file if file[-3:] != 'jpg' and file != 'sign exit.png' else 'cooler.png'
               for file in os.listdir('data/levels/decorative_objects')]
    for _ in range(5):
        objects.remove('cooler.png')

    for _ in range(10):
        Object(load_image(f'levels/decorative_objects/{random.choice(objects)}'),
               random.choice(coords_x), random.choice(coords_y))

    # buttons_sprites = pygame.sprite.Group()
    tiles = get_background(bg_image)
    count = 0

    while True:

        ticks = pygame.time.get_ticks()
        if ticks % FPS:
            count += 0.5

        draw_backgound(tiles, int(count % 32), bg_image)

        all_sprites.draw(screen)
        all_sprites.update()

        screen.blit(string_rendered, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_buttons['Играть'].click_check(event.pos):
                    print('Играй')
                    levels()
                if main_menu_buttons['Выбор персонажа'].click_check(event.pos):
                    print('Выбери персонажа')
                    character_selection()
                if main_menu_buttons['Статистика'].click_check(event.pos):
                    print('Смотри статистику')
                if main_menu_buttons['Настройки'].click_check(event.pos):
                    print('Настрой себя')
                if main_menu_buttons['Выход'].click_check(event.pos):
                    terminate()

        for button in main_menu_buttons:
            main_menu_buttons[button].update(screen)
            main_menu_buttons[button].change_colour(pygame.mouse.get_pos())

        pygame.display.flip()
        clock.tick(FPS)


def levels():
    pygame.display.set_caption('Escape from Kvantorium - Выбор уровня')

    text = 'Выберите уровень'

    """fon = pygame.transform.scale(load_image('bg.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))"""
    font = pygame.font.Font(None, 64)

    string_rendered = font.render(text, 1, (28, 28, 28))
    text_rect = string_rendered.get_rect(center=(WIDTH // 2, HEIGHT // 10))
    screen.blit(string_rendered, text_rect)

    # buttons_sprites = pygame.sprite.Group()

    tiles = get_background(bg_image1)
    # print('ok')
    count = 0

    while True:

        ticks = pygame.time.get_ticks()
        if ticks % FPS:
            count += 0.5

        draw_backgound(tiles, int(count % 32), bg_image1)
        screen.blit(string_rendered, text_rect)
        return_btn.update(screen)
        return_btn.change_colour(pygame.mouse.get_pos())

        for button in level_btns:
            button.update(screen)
            button.change_colour(pygame.mouse.get_pos())

        for star_group in stars:
            for star in star_group:
                star.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_btn.click_check(event.pos):
                    return
                for button in level_btns:
                    if button.click_check(event.pos):
                        print('level' + str(level_btns.index(button) + 1))
                        if level_btns.index(button) + 1 == 1:  #  проверка какой уровень
                            intro_maker(['Вы задержались допоздна в Кванториуме, пытаясь успеть доделать проект, '
                                        'но вы не успели.', 'Бегите!'], (255, 255, 255))
                        elif level_btns.index(button) + 1 == 2:
                            intro_maker(['Спаси своего друга Ярика'], (255, 255, 255))
                        elif level_btns.index(button) + 1 == 5:
                            intro_maker(['Спаси своего друга Сашу'], (255, 255, 255))
                        elif level_btns.index(button) + 1 == 9:
                            intro_maker(['Спаси своего друга Ваню'], (255, 255, 255))
                        elif level_btns.index(button) + 1 == 7:
                            intro_maker(['Спаси своего друга Влада'], (255, 255, 255))
                        elif level_btns.index(button) + 1 == 10:
                            intro_maker(['БЕГИ!', 'БEГИ!', 'БЕГИ!'], (255, 0, 0))  # неправильно работает
                        all_sprites = pygame.sprite.Group()
                        hero = Hero(200, 40)
                        labirint = Labirint('level1.tmx', [*range(1, 31)], 18)
                        all_sprites.add(hero, labirint.sprites)
                        level_displayer(labirint, hero, all_sprites)
                        level_displayer(1, labirint, hero)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(FPS)


def character_selection():
    pygame.display.set_caption('Escape from Kvantorium - Выбор персонажа')

    screen.fill((0, 0, 0))

    barrier = pygame.Surface((10, 10))
    barrier_rect = pygame.Rect(100, 400, 100, 100)

    tiles = get_background(bg_image1)
    # print('ok')
    count = 0

    while True:

        ticks = pygame.time.get_ticks()
        if ticks % FPS:
            count += 0.5

        draw_backgound(tiles, int(count % 32), bg_image_character)

        screen.blit(person_image, person_image.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        #screen.blit(barrier, barrier_rect)
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 10)
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 2, HEIGHT // 3), (WIDTH, HEIGHT // 3), 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(FPS)


def level_displayer(level_number, labirint, hero):
    pygame.display.set_caption(f'Escape from Kvantorium - {level_number} уровень')


def level_displayer(labirint, hero, all_sprites):
    left = right = up = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if pygame.key.get_pressed()[pygame.K_a]:
                    left = True
                if pygame.key.get_pressed()[pygame.K_d]:
                    right = True
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    up = True
            if event.type == pygame.KEYUP:
                if not(pygame.key.get_pressed()[pygame.K_a]):
                    left = False
                if not(pygame.key.get_pressed()[pygame.K_d]):
                    right = False
                if not(pygame.key.get_pressed()[pygame.K_SPACE]):
                    up = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(labirint.is_free(event.pos))
                print(event.pos)
                print(hero.get_position())

        if labirint.is_free(hero.get_position()):
            hero.onGround = False
        else:
            hero.onGround = True
        labirint.render(screen)
        hero.move(left, right, up, labirint.platform)
        hero.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main_menu()
