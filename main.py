import random  # необходимые импорты
import pygame
import sys
import os
from button import Button
from settings import *
from functions import load_image, Object, Border, all_sprites, full_wrapper
from level_generation import Labirint
from hero import Hero
from star import Star
from data_levels import students, students_lst, level
from camera import Camera, camera_configure
from timer import Timer
from graffiti import Graffiti
from enemy import Enemy
from winstar import Stars
import sqlite3

pygame.init()  # инициализация pygame

pygame.display.set_caption('Проект')  # изменяем название окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # устанавливаем размеры экрана
icon = load_image('pictures/kvantorium_logo.png')  # добавляем иконку окна
pygame.display.set_icon(icon)  # ставим нашу иконку вместо стандартной

clock = pygame.time.Clock()
con = sqlite3.connect('data/EFK.db')
cur = con.cursor()

main_font = pygame.font.Font(None, 64)  # основной шрифт
mini_font = pygame.font.Font(None, 32)  # маленький шрифт
big_font = pygame.font.Font(None, 128)  # большой шрифт
main_offset = (WIDTH + HEIGHT) // 31  # основной отступ от краёв экрана

bg_image = load_image('pictures/pattern6.png')
bg_image1 = load_image('pictures/pattern13.png')
bg_image_character = load_image('pictures/pattern9.png')
bg_image_game_over = load_image('pictures/pattern16.png')

ENEMY_EVENT_TYPE = 30


def get_image(sheet, frame, line, width, height, scale):  # берём часть изображения
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (width * (frame - 1), height * (line - 1), width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((9, 9, 9))  # убираем задний фон
    return image


reasons = ''  # уровень
selected_character = 'Никита'  # изначально выбранный персонаж
person_sheet = None  # загружаем картинку персонажа
person_image = get_image(load_image(f'characters/{selected_character}.png'), 1, 1, 48, 96, 6)


def storyboard():  # для раскадровки персонажей
    frame_and_line = [(2, 1, '_0.png'), (1, 2, '_rl2.png'), (3, 2, '_rl3.png'), (7, 2, '_rl1.png'), (9, 2, '_rl4.png'),
                      (1, 3, '_rr2.png'), (3, 3, '_rr3.png'), (7, 3, '_rr4.png'), (9, 3, '_rr1.png')]
    for char in ['Иван Дмитриевич']:  # список персонажей для раскадровки
        for f in frame_and_line:
            char_sheet = load_image(f'characters/{char}.png')
            image = get_image(char_sheet, f[0], f[1], 48, 96, 1)
            image = image.subsurface((8, 24, 32, 70))
            pygame.image.save(image, f'data/characters/animation/{char + f[2]}')


id_texture = [*range(1, 12), 16, 17, 19, 28, 29, 30]

button_image = load_image('pictures/button1.png')
button_image1 = load_image('pictures/button2.png')
button_image2 = load_image('pictures/button3.png')

select_btn = Button(WIDTH // 6 * 2, HEIGHT - main_offset, button_image, button_image1, 'Выбрать', 4)
selected_btn = Button(WIDTH // 6 * 2, HEIGHT - main_offset, button_image2, button_image2, 'Выбрано', 4)

button_list = ['Играть', 'Выбор персонажа', 'Статистика', 'Настройки', 'Выход']  # список кнопок
main_menu_buttons = {}
for i in range(len(button_list)):
    main_menu_buttons[button_list[i]] = Button(WIDTH // 2, HEIGHT // 7 * (i + 2),
                                               button_image, button_image1, button_list[i], 4)

arrow_right = load_image('pictures/arrow_right.png')
arrow_right_ = load_image('pictures/arrow_right_.png')
arrow_left = pygame.transform.rotate(arrow_right, 180)
arrow_left_ = pygame.transform.rotate(arrow_right_, 180)

return_btn = Button(main_offset, main_offset, load_image('pictures/return_btn.png'),
                    load_image('pictures/return_btn_.png'))  # кнопка возврата

arrow_right_btn = Button(WIDTH // 6 * 4 - main_offset, HEIGHT - main_offset, arrow_right, arrow_right_)
arrow_left_btn = Button(main_offset, HEIGHT - main_offset, arrow_left, arrow_left_)

level_btns = []

for i in range(1, 11):
    level_btns.append(Button(WIDTH // 6 * 5 if (i % 5) == 0 else WIDTH // 6 * (i % 5),
                             HEIGHT // 3 if i < 6 else HEIGHT // 3 * 2,
                             load_image(f'pictures/{i}.png'),
                             load_image(f'pictures/{i}_.png'), None, WIDTH // 240))

star_active = load_image('pictures/star_active.png')
star_inactive = load_image('pictures/star_inactive.png')


def update():  # обновление звездочек в меню
    a = 1
    star = []
    for button in level_btns:
        base = cur.execute("""SELECT stars FROM levels
                        WHERE number = ?""", (str(a),)).fetchall()
        if base == [('0',)]:
            star.append([Star(star_active, star_inactive, 'left', button),
                         Star(star_active, star_inactive, 'right', button),
                         Star(star_active, star_inactive, 'middle', button)])
        elif base == [('1',)]:
            star.append([Star(star_active, star_active, 'left', button),
                         Star(star_active, star_inactive, 'right', button),
                         Star(star_active, star_inactive, 'middle', button)])
        elif base == [('2',)]:
            star.append([Star(star_active, star_active, 'left', button),
                         Star(star_active, star_inactive, 'right', button),
                         Star(star_active, star_active, 'middle', button)])
        else:
            star.append([Star(star_active, star_active, 'left', button),
                         Star(star_active, star_active, 'right', button),
                         Star(star_active, star_active, 'middle', button)])
        a += 1
    return star


restart_btn = Button(main_offset, main_offset, load_image('pictures/restart_btn.png'),
                     load_image('pictures/restart_btn_.png'))

pause_btn = Button(main_offset * 1.2 + return_btn.image.get_width(), main_offset, load_image('pictures/pause.png'),
                   load_image('pictures/pause_.png'))

resume_btn = Button(WIDTH // 5 * 3, HEIGHT // 2, load_image('pictures/resume.png'),
                    load_image('pictures/resume_.png'), None, 4)

home_btn = Button(WIDTH // 5 * 2, HEIGHT // 2, load_image('pictures/home_btn.png'),
                  load_image('pictures/home_btn_.png'), None, 4)

coords_x = [i for i in range(-100, -50)] + [j for j in range(WIDTH + 50, WIDTH + 100)]
coords_y = [i for i in range(-100, -50)] + [j for j in range(HEIGHT + 50, HEIGHT + 100)]
objects = []  # объекты, летающие в главном меню
for file in os.listdir('data/levels/decorative_objects'):
    if file[-3:] != 'jpg' and file != 'sign exit.png' and file != 'фон.png':  # не используем неподходящие картинки
        objects.append(file)

for _ in range(10):  # создаём 10 объектов со случайными начальными координатами
    Object(load_image(f'levels/decorative_objects/{random.choice(objects)}'),
           random.choice(coords_x), random.choice(coords_y))


# заставки к уровням
def intro_maker(message, colour=(255, 255, 255)):
    messages = full_wrapper(message, WIDTH // 16)
    cur_message = 0
    message_offsets = [50 * i for i in range(len(messages))]
    alpha, direction = 0, 2
    font = pygame.font.Font(None, 32)
    count, speed = 0, 3
    skip_text = mini_font.render('Нажмите ЛЮБУЮ клавишу, чтобы продолжить', True, (255, 255, 255))
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
            string = mini_font.render(message, True, colour)
            string_rect = string.get_rect(center=(WIDTH // 2, HEIGHT // 2 + message_offsets[messages.index(message)]))
            screen.blit(string, string_rect)

        if count < len(messages[cur_message]) * speed:
            count += 1
        elif cur_message < len(messages) - 1:
            count = 0
            cur_message += 1
            for i in range(len(message_offsets)):
                message_offsets[i] -= 25

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


def draw_vertical_backgound(tiles, offset, image):
    # print(offset)
    for tile in tiles:
        screen.blit(image, (tile[0] - offset, tile[1]))


def terminate():
    pygame.quit()
    sys.exit()


def main_menu():  # главное меню
    pygame.display.set_caption('Escape from Kvantorium')

    text = 'Escape from Kvantorium'

    string_rendered = main_font.render(text, 1, (28, 28, 28))
    string_rendered_shadow = main_font.render(text, 1, (1, 1, 1))
    text_rect = string_rendered.get_rect(center=(WIDTH // 2, HEIGHT // 10))
    screen.blit(string_rendered, text_rect)
    offscreen = 200

    Border(-offscreen, -offscreen, WIDTH + offscreen, -offscreen)  # - верхний
    Border(-offscreen, HEIGHT + offscreen, WIDTH + offscreen, HEIGHT + offscreen)  # - нижний
    Border(-offscreen, -offscreen, -offscreen, HEIGHT + offscreen)  # | левый
    Border(WIDTH + offscreen, -offscreen, WIDTH + offscreen, HEIGHT + offscreen)  # | правый

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

        screen.blit(string_rendered_shadow, (text_rect.x + 2, text_rect.y + 2))
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
                    character_selection(selected_character)
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

    string_rendered = main_font.render(text, 1, (28, 28, 28))
    text_rect = string_rendered.get_rect(center=(WIDTH // 2, HEIGHT // 10))
    screen.blit(string_rendered, text_rect)

    # buttons_sprites = pygame.sprite.Group()

    tiles = get_background(bg_image1)
    count = 0
    stars = update()
    while True:

        ticks = pygame.time.get_ticks()
        if ticks % FPS:
            count += 0.5

        draw_backgound(tiles, int(count % 32), bg_image_character)
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
                        global reasons
                        print('level' + str(level_btns.index(button) + 1))
                        reasons = level_btns.index(button)
                        if level_btns.index(button) + 1 == 1:  # проверка какой уровень
                            intro_maker(['Вы задержались допоздна в Кванториуме, пытаясь успеть '
                                         'доделать проект, но вы не успели.', 'Бегите!'], (255, 255, 255))
                        elif level_btns.index(button) + 1 == 2:
                            intro_maker(['Спаси своего друга Ярика'], (255, 255, 255))
                        elif level_btns.index(button) + 1 == 5:
                            intro_maker(['Спаси своего друга Сашу'], (255, 255, 255))
                        elif level_btns.index(button) + 1 == 7:
                            intro_maker(['Спаси своего друга Влада'], (255, 255, 255))
                        elif level_btns.index(button) + 1 == 9:
                            intro_maker(['Спаси своего друга Ваню'], (255, 255, 255))
                        elif level_btns.index(button) + 1 == 10:
                            intro_maker(['БЕГИ!', 'БEГИ!', 'БЕГИ!'], (255, 0, 0))
                        new_game(level_btns.index(button))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(FPS)


# меню выбора персонажей
def character_selection(character):
    global selected_character
    pygame.display.set_caption('Escape from Kvantorium - Выбор персонажа')

    buttons = [return_btn]
    left, right, selected = True, True, False
    if students_lst.index(character) == 0:
        buttons.append(arrow_right_btn)
        left = False
    elif students_lst.index(character) == len(students_lst) - 1:
        buttons.append(arrow_left_btn)
        right = False
    else:
        buttons.append(arrow_right_btn)
        buttons.append(arrow_left_btn)
    if character == selected_character:
        buttons.append(selected_btn)
        selected = True
    else:
        buttons.append(select_btn)

    name = main_font.render(character, 1, (28, 28, 28))  # имя персонажа
    name_rect = name.get_rect(center=(WIDTH // 6 * 5, HEIGHT // 6))  # имя располагается в правой верхней части экрана
    info = full_wrapper([students[character]], 25)  # информация о персонаже
    info_offsets = [25 * i - (12 * len(info)) for i in range(len(info))]  # информация находится в правой нижней части

    person_sheet = load_image(f'characters/{character}.png')
    person_image = get_image(person_sheet, 2, 1, 48, 96, 6)

    tiles = get_background(bg_image1)
    count = 0

    while True:

        if pygame.time.get_ticks() % FPS:
            count += 0.5

        draw_backgound(tiles, int(count % 32), bg_image_character)
        pygame.draw.rect(screen, pygame.Color('#f6f4fc'), (WIDTH // 6 * 4, 0, WIDTH, HEIGHT))

        for btn in buttons:
            btn.update(screen)
            btn.change_colour(pygame.mouse.get_pos())

        screen.blit(name, name_rect)  # отрисовываем имя
        for line in info:  # отрисовываем информацию построчно
            string = mini_font.render(line, True, (28, 28, 28))
            string_rect = string.get_rect(center=(WIDTH // 6 * 5, HEIGHT // 6 * 4 + info_offsets[info.index(line)]))
            screen.blit(string, string_rect)

        # отрисовываем картинку персонажа
        screen.blit(person_image, person_image.get_rect(center=(WIDTH // 6 * 2, HEIGHT // 2 - HEIGHT * 0.1)))

        # рисуем линии-разделители
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 6 * 4, 0), (WIDTH // 6 * 4, HEIGHT), 10)
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 6 * 4, HEIGHT // 3), (WIDTH, HEIGHT // 3), 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and left:  # переходим на кнопку a или стрелку влево
                    character_selection(students_lst[students_lst.index(character) - 1])
                if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and right:  # переходим на кнопку d или стрелку вправо
                    character_selection(students_lst[students_lst.index(character) - 1])
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_btn.click_check(event.pos):
                    main_menu()
                if arrow_left_btn.click_check(event.pos) and left:  # стрелка влево
                    character_selection(students_lst[students_lst.index(character) - 1])
                if arrow_right_btn.click_check(event.pos) and right:  # стрелка вправо
                    character_selection(students_lst[students_lst.index(character) + 1])
                if buttons[-1].click_check(event.pos) and not selected:  # если персонаж не выбран, выбираем
                    selected_character = character
                    buttons[-1] = selected_btn
                    selected = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(FPS)


def new_game(level_number):
    global reasons
    person = selected_character
    hero = Hero(*level[level_number]['spawn'], person, reasons)
    # enemy = Enemy(*level[level_number]['spawn_dop'])
    all_sprites = pygame.sprite.Group()
    labirint = Labirint(level[level_number]['level_map'], id_texture, 18)

    total_level_width = labirint.width * 32  # Высчитываем фактическую ширину уровня
    total_level_height = labirint.height * 32  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    all_sprites.add(labirint.sprites, hero)
    level_displayer(level_number, labirint, hero, all_sprites, camera)


def end(time):  # окончание уровня победой
    global reasons
    pygame.display.set_caption('Escape from Kvantorium - WIN')
    text = 'WIN'
    string_rendered = main_font.render(text, 1, (28, 28, 28))
    string_rendered_shadow = main_font.render(text, 1, (1, 1, 1))
    text_rect = string_rendered.get_rect(center=(WIDTH // 2, HEIGHT // 10))
    screen.blit(string_rendered, text_rect)
    offscreen = 200
    seconds = '0' + str(time % 60) if time % 60 < 10 else str(time % 60)
    minutes = '0' + str(time // 60) if time // 60 < 10 else str(time // 60)
    text1 = 'YOUR TIME: ' + minutes + ':' + seconds
    string_rendern = main_font.render(text1, 1, (28, 28, 28))
    string_rendern_shadow = main_font.render(text1, 1, (1, 1, 1))
    text_rect1 = string_rendern.get_rect(center=(WIDTH // 2, 175))
    screen.blit(string_rendern, text_rect1)
    print(text1)
    Border(-offscreen, -offscreen, WIDTH + offscreen, -offscreen)  # - верхний
    Border(-offscreen, HEIGHT + offscreen, WIDTH + offscreen, HEIGHT + offscreen)  # - нижний
    Border(-offscreen, -offscreen, -offscreen, HEIGHT + offscreen)  # | левый
    Border(WIDTH + offscreen, -offscreen, WIDTH + offscreen, HEIGHT + offscreen)  # | правый
    # buttons_sprites = pygame.sprite.Group()
    tiles = get_background(bg_image1)
    count = 0
    stars1 = []
    if time <= level[reasons]['three']:
        stars1.append([Stars(star_active, 'left', 480, 300),
                       Stars(star_active, 'right', 480, 300),
                       Stars(star_active, 'middle', 480, 300)])
        sp = 3
    elif level[reasons]['two'] >= time > level[reasons]['three']:
        stars1.append([Stars(star_active, 'left', 480, 300),
                       Stars(star_inactive, 'right', 480, 300),
                       Stars(star_active, 'middle', 480, 300)])
        sp = 2
    else:
        stars1.append([Stars(star_active, 'left', 480, 300),
                       Stars(star_inactive, 'right', 480, 300),
                       Stars(star_inactive, 'middle', 480, 300)])
        sp = 1
    base = cur.execute("""SELECT stars FROM levels
            WHERE number = ?""", (int(reasons) + 1,)).fetchall()
    con.commit()
    if sp > int(base[0][0]):  # изменение количества звезд
        sp1 = base
        sp1[0] = tuple(str(sp))
        print(sp1)
        cur.execute("""UPDATE levels
        SET stars = ?
        WHERE number = ?""", (sp, int(reasons) + 1)).fetchall()
        con.commit()
        cur.execute("""UPDATE levels
                SET state = 'разблок'
                WHERE number = ?""", (str(int(reasons) + 2),)).fetchall()
        con.commit()
        update()
    alpha, direction = 0, 2
    skip_text = mini_font.render('Нажмите ЛЮБУЮ клавишу, чтобы перейти к выбору уровня',
                                 True, (0, 0, 0))
    base = cur.execute("""SELECT time FROM levels
                WHERE number = ?""", (int(reasons) + 1,)).fetchall()
    base1 = int(base[0][0].split(':')[0])
    base2 = int(base[0][0].split(':')[1])
    if base1 * 60 + base2 > time or base1 * 60 + base2 == 0:  # изменение времени
        cur.execute("""UPDATE levels
                SET time = ?
                WHERE number = ?""", (minutes + ':' + seconds, int(reasons) + 1)).fetchall()
        con.commit()
    skip_text.set_alpha(alpha)
    while True:
        ticks = pygame.time.get_ticks()
        if ticks % FPS:
            count += 0.5
        draw_backgound(tiles, int(count % 32), bg_image_character)
        all_sprites.draw(screen)
        all_sprites.update()
        alpha += direction
        if alpha == 0:
            direction = 2
        skip_text.set_alpha(alpha)
        screen.blit(skip_text, skip_text.get_rect(center=(WIDTH // 2, HEIGHT * 0.8)))
        screen.blit(string_rendered_shadow, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(string_rendered, text_rect)
        screen.blit(string_rendern_shadow, (text_rect1.x + 2, text_rect1.y + 2))
        screen.blit(string_rendern, text_rect1)
        for star_group in stars1:
            for star in star_group:
                star.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                levels()
        pygame.display.flip()
        clock.tick(FPS)


# отображает уровень
def level_displayer(level_number, labirint, hero, all_sprites, camera):
    global reasons
    pygame.display.set_caption(f'Escape from Kvantorium - {level_number + 1} уровень')
    left = right = up = False
    timer = Timer(WIDTH // 2, HEIGHT * 0.07, mini_font)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    graffiti_list = [Graffiti([300, 122], 'LEFT')]
    drawing = False
    draw_new_graffiti = True

    while True:
        bg = pygame.Surface((WIDTH, HEIGHT))  # Создание видимой поверхности
        # будем использовать как фон
        bg.fill(pygame.Color('#004400'))  # Заливаем поверхность сплошным цветом
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                timer.update()
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                terminate()
            """if event.type == ENEMY_EVENT_TYPE:
                enemy.move(labirint.find_path_step(enemy.get_position(), hero.get_position()[:2]))"""
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    if draw_new_graffiti:
                        draw_new_graffiti = False
                        drawing = True
                        if keys[pygame.K_w] or keys[pygame.K_UP]:
                            graffiti_list.append(Graffiti(pygame.mouse.get_pos(), 'UP'))
                        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                            graffiti_list.append(Graffiti(pygame.mouse.get_pos(), 'RIGHT'))
                        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                            graffiti_list.append(Graffiti(pygame.mouse.get_pos(), 'DOWN'))
                        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                            graffiti_list.append(Graffiti(pygame.mouse.get_pos(), 'LEFT'))
                        else:
                            draw_new_graffiti = True
                            drawing = False
                    if drawing:
                        if keys[pygame.K_w] or keys[pygame.K_UP]:
                            graffiti_list[-1].change_direction('UP')
                        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                            graffiti_list[-1].change_direction('RIGHT')
                        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                            graffiti_list[-1].change_direction('DOWN')
                        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                            graffiti_list[-1].change_direction('LEFT')
                    if keys[pygame.K_q]:
                        if drawing:
                            graffiti_list = graffiti_list[:-1]
                            draw_new_graffiti = True
                            drawing = False
                if event.key == pygame.K_ESCAPE:
                    pause()
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    left = True
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    right = True
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    if pygame.key.get_pressed()[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
                        up = 2
                elif keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
                    up = 1
            if event.type == pygame.KEYUP:
                if not (keys[pygame.K_a]) and not (keys[pygame.K_LEFT]):
                    left = False
                if not (keys[pygame.K_d]) and not (keys[pygame.K_RIGHT]):
                    right = False
                if not (keys[pygame.K_SPACE]) and not (keys[pygame.K_w]) and not (keys[pygame.K_UP]):
                    up = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.click_check(event.pos):  # перезапускает уровень
                    new_game(level_number)
                if pause_btn.click_check(event.pos):
                    left = right = False
                    pause()
                if drawing:
                    draw_new_graffiti = True
                    drawing = False
                print(event.pos)
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    graffiti_list[-1].update(pygame.mouse.get_pos())

        if labirint.is_free(hero.get_position()):
            hero.onGround = False

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.move(left, right, up, labirint.platform)  # передвижение
        # enemy.move(labirint.find_path_step(enemy.get_position(), hero.get_position()))
        for e in all_sprites:
            screen.blit(e.image, camera.apply(e))

        for graffiti in graffiti_list:
            screen.blit(graffiti.image, camera.apply(graffiti))

        timer.draw(screen)

        restart_btn.update(screen)
        restart_btn.change_colour(pygame.mouse.get_pos())
        pause_btn.update(screen)
        pause_btn.change_colour(pygame.mouse.get_pos())
        if level[reasons]['one'] <= timer.get_time():
            game_over('Время кончилось')
        if hero.exit():  # если игрок дошел до выхода
            timer.pauses()
            end(timer.get_time())
        pygame.display.flip()
        clock.tick(FPS)


# пауза в уровне
def pause():
    pygame.display.set_caption(f'Escape from Kvantorium - пауза')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.click_check(event.pos):
                    return
                if home_btn.click_check(event.pos):
                    main_menu()
                    # game_over()

        pygame.draw.rect(screen, pygame.Color('grey'), (WIDTH // 4, HEIGHT // 3, WIDTH // 4 * 2, HEIGHT // 3))
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 4, HEIGHT // 3), (WIDTH // 4 * 3, HEIGHT // 3), 10)
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 4, HEIGHT // 3 * 2), (WIDTH // 4 * 3, HEIGHT // 3 * 2), 10)
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 4, HEIGHT // 3), (WIDTH // 4, HEIGHT // 3 * 2), 10)
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 4 * 3, HEIGHT // 3), (WIDTH // 4 * 3, HEIGHT // 3 * 2), 10)
        home_btn.update(screen)
        home_btn.change_colour(pygame.mouse.get_pos())
        resume_btn.update(screen)
        resume_btn.change_colour(pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def game_over(reason='Вас поймали'):  # проигрыш
    pygame.display.set_caption(f'Escape from Kvantorium - game over')
    game_text = big_font.render('Game', 1, (28, 28, 28))
    game_text_shadow = big_font.render('Game', 1, (1, 1, 1))
    over_text = big_font.render('Over', 1, (28, 28, 28))
    over_text_shadow = big_font.render('Over', 1, (1, 1, 1))
    reason_text = main_font.render(reason, 1, (28, 28, 28))
    reason_text_shadow = main_font.render(reason, 1, (1, 1, 1))

    tiles_left = get_background(bg_image_game_over)
    tiles_right = get_background(bg_image_game_over)
    walls_collided = False

    count = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.click_check(event.pos) and walls_collided:
                    return
                if home_btn.click_check(event.pos) and walls_collided:
                    main_menu()

        screen.fill((0, 0, 0))

        if count < WIDTH // 2:
            count += 7
        else:
            count = WIDTH // 2
            walls_collided = True

        # pygame.draw.rect(screen, (122, 119, 155), (0, 0, 0 + count, HEIGHT))
        # pygame.draw.rect(screen, (122, 119, 155), (WIDTH - count, 0, WIDTH, HEIGHT))

        draw_vertical_backgound(tiles_left, WIDTH - count, bg_image_game_over)
        draw_vertical_backgound(tiles_right, -WIDTH + count, bg_image_game_over)

        screen.blit(game_text_shadow, game_text.get_rect(center=(-WIDTH // 7 + count + 2, HEIGHT // 7 + 2)))
        screen.blit(over_text_shadow, game_text.get_rect(center=(WIDTH + WIDTH // 7 - count + 2, HEIGHT // 7 + 2)))
        screen.blit(game_text, game_text.get_rect(center=(-WIDTH // 7 + count, HEIGHT // 7)))
        screen.blit(over_text, game_text.get_rect(center=(WIDTH + WIDTH // 7 - count, HEIGHT // 7)))
        # pygame.draw.line(screen, (39, 36, 46), (WIDTH // 6 * 4, HEIGHT // 3), (WIDTH, HEIGHT // 3), 10)
        if walls_collided:
            screen.blit(reason_text_shadow, game_text.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 7 * 2 + 2)))
            screen.blit(reason_text, game_text.get_rect(center=(WIDTH // 2, HEIGHT // 7 * 2)))
            home_btn.update(screen)
            home_btn.change_colour(pygame.mouse.get_pos())
            resume_btn.update(screen)
            resume_btn.change_colour(pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main_menu()