import random  # необходимые импорты
import pygame
import sys
import os
from files.button import Button, CheckButton
from files.settings import *
from files.functions import load_image, Object, Border, all_sprites, full_wrapper, Text
from files.level_generation import Labirint
from files.hero import Hero
from files.star import Star
from files.data_levels import students, students_lst, level, spawn_teachers
from files.camera import Camera, camera_configure
from files.timer import Timer
from files.graffiti import Graffiti
from files.people import Students, Teacher
from files.winstar import Stars
import sqlite3

pygame.init()  # инициализация pygame

pygame.display.set_caption('Проект')  # изменение названия окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # установка размеров экрана
icon = load_image('pictures/kvantorium_logo.png')  # добавление иконки окна
pygame.display.set_icon(icon)  # использвание нашей иконки вместо стандартной

clock = pygame.time.Clock()

# создание шрифтов
main_font = pygame.font.Font(None, 64)  # основной шрифт
mini_font = pygame.font.Font(None, 32)  # маленький шрифт
big_font = pygame.font.Font(None, 128)  # большой шрифт
hero_font = pygame.font.Font(None, 20)  # шрифт для имён персонажей

main_offset = (WIDTH + HEIGHT) // 31  # основной отступ от краёв экрана

# загрузка изображений
bg_image = load_image('pictures/pattern6.png')
bg_image1 = load_image('pictures/pattern13.png')
bg_image_character = load_image('pictures/pattern9.png')
bg_image_game_over = load_image('pictures/pattern16.png')
button_image = load_image('pictures/button1.png')
button_image1 = load_image('pictures/button2.png')
button_image2 = load_image('pictures/button3.png')
arrow_right = load_image('pictures/arrow_right.png')
arrow_right_ = load_image('pictures/arrow_right_.png')
arrow_left = pygame.transform.rotate(arrow_right, 180)
arrow_left_ = pygame.transform.rotate(arrow_right_, 180)
star_active = load_image('pictures/star_active.png')
star_inactive = load_image('pictures/star_inactive.png')
empty_image = load_image('pictures/empty_btn.png')
empty_image_ = load_image('pictures/empty_btn_.png')
checked_image = load_image('pictures/checked_btn.png')
checked_image_ = load_image('pictures/checked_btn_.png')
button_lock = load_image('pictures/button_lock.png')


def get_image(sheet, frame, line, width, height, scale):  # берём часть изображения
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (width * (frame - 1), height * (line - 1), width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((9, 9, 9))  # убираем задний фон
    return image


def get_text(text, font, coords, colour=(28, 28, 28)):
    text_rendered = font.render(text, 1, colour)
    text_rect = text_rendered.get_rect(center=coords)

    return text_rendered, text_rect


def draw_text(surface, *texts):
    for text in texts:
        surface.blit(text[0], text[1])


def draw_rect(surface, rect, center):
    rect = pygame.Rect(rect)
    rect.center = center
    pygame.draw.rect(surface, (200, 200, 200), rect)


con = sqlite3.connect('data/EFK.db')
cur = con.cursor()

number = ''  # уровень
selected_character = cur.execute("""SELECT character FROM data""").fetchone()[0]  # изначально выбранный персонаж
control_settings = {  # настройки управления
    'WASD': cur.execute("""SELECT control_wasd FROM data""").fetchone()[0],
    'ARROWS': cur.execute("""SELECT control_arrows FROM data""").fetchone()[0]}


def storyboard():  # для раскадровки персонажей
    frame_and_line = [(2, 1, '_0.png'), (1, 2, '_rl2.png'), (3, 2, '_rl3.png'), (7, 2, '_rl1.png'), (9, 2, '_rl4.png'),
                      (1, 3, '_rr2.png'), (3, 3, '_rr3.png'), (7, 3, '_rr4.png'), (9, 3, '_rr1.png')]
    for char in ['Илья']:  # список персонажей для раскадровки
        for f in frame_and_line:
            char_sheet = load_image(f'characters/{char}.png')
            image = get_image(char_sheet, f[0], f[1], 48, 96, 1)
            image = image.subsurface((8, 24, 32, 70))
            pygame.image.save(image, f'data/characters/animation/{char + f[2]}')


id_texture = [*range(1, 12), 16, 17, 19, 28, 29, 30]  # id текстур уровней

# создание экземпляров кнопки
# кнопки выбора меню персонажей
select_btn = Button(WIDTH // 6 * 2, HEIGHT - main_offset, button_image, button_image1, 'Выбрать', 4)
selected_btn = Button(WIDTH // 6 * 2, HEIGHT - main_offset, button_image2, button_image2, 'Выбрано', 4)
btn_lock = Button(WIDTH // 6 * 2, HEIGHT - main_offset, button_lock, button_lock, '', 4)

# кнопки главного меню
button_list = ['Играть', 'Выбор персонажа', 'Статистика', 'Настройки', 'Выход']  # список кнопок
main_menu_buttons = {}
for i in range(len(button_list)):
    main_menu_buttons[button_list[i]] = Button(WIDTH // 2, HEIGHT // 7 * (i + 2),
                                               button_image, button_image1, button_list[i], 4)

return_btn = Button(main_offset, main_offset, load_image('pictures/return_btn.png'),
                    load_image('pictures/return_btn_.png'))  # кнопка возврата

# кнопки вправо и влево
arrow_right_btn = Button(WIDTH // 6 * 4 - main_offset, HEIGHT - main_offset, arrow_right, arrow_right_)
arrow_left_btn = Button(main_offset, HEIGHT - main_offset, arrow_left, arrow_left_)

# кнопки для уровней
level_btns = []

for i in range(1, 11):
    bases = cur.execute("""SELECT state FROM levels
                        WHERE number = ?""", (str(i),)).fetchall()
    if bases[0][0] == 'разблок':
        level_btns.append(Button(WIDTH // 6 * 5 if (i % 5) == 0 else WIDTH // 6 * (i % 5),
                                 HEIGHT // 3 if i < 6 else HEIGHT // 3 * 2,
                                 load_image(f'pictures/{i}.png'),
                                 load_image(f'pictures/{i}_.png'), None, WIDTH // 240))
    else:
        level_btns.append(Button(WIDTH // 6 * 5 if (i % 5) == 0 else WIDTH // 6 * (i % 5),
                                 HEIGHT // 3 if i < 6 else HEIGHT // 3 * 2,
                                 load_image('pictures/locked_btn.png'),
                                 load_image('pictures/locked_btn.png'), None, WIDTH // 240))

check_btn_WASD = CheckButton(WIDTH // 5, HEIGHT // 6 * 2, empty_image, empty_image_, checked_image, checked_image_,
                             control_settings['WASD'], 4)
check_btn_ARROWS = CheckButton(WIDTH // 5, HEIGHT // 6 * 4, empty_image, empty_image_, checked_image, checked_image_,
                               control_settings['ARROWS'], 4)


def stars_update():  # обновление звездочек в меню
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


# кнопка рестарта
restart_btn = Button(main_offset, main_offset, load_image('pictures/restart_btn.png'),
                     load_image('pictures/restart_btn_.png'))

# кнопка паузы
pause_btn = Button(main_offset * 1.2 + return_btn.image.get_width(), main_offset, load_image('pictures/pause.png'),
                   load_image('pictures/pause_.png'))

#
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
    message_offsets = [50 * n for n in range(len(messages))]
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


# создание тайлов для заднего плана
def get_background(image):
    tiles = []
    width, height = image.get_width(), image.get_height()
    for i in range(WIDTH // width + 2):
        for j in range(HEIGHT // height + 2):
            tiles.append((i * width, j * height))
    return tiles


# отрисовка заднего плана
def draw_backgound(tiles, offset, image):
    for tile in tiles:
        screen.blit(image, (tile[0] - offset, tile[1] - offset))


def update_and_draw_backgroud(count, tiles, image):
    if pygame.time.get_ticks() % FPS:
        count += 0.5

    draw_backgound(tiles, int(count % 32), image)

    return count


def draw_game_over_background(tiles, offset, image):
    for tile in tiles:
        screen.blit(image, (tile[0] - offset, tile[1]))


# завершить программу
def terminate():
    pygame.quit()
    sys.exit()


def leader_board():  # вывод статистики из бд
    pygame.display.set_caption('Escape from Kvantorium - Статистика')
    screen.fill((133, 112, 172))
    pygame.draw.rect(screen, (255, 255, 255), (30, 30, 905, 553))
    text = cur.execute("""SELECT number, stars, time, atempts FROM levels where state = 'разблок'""").fetchall()
    h = HEIGHT // 10 - 1

    a = ['звёзды', 'время', 'попытки']
    string_rendered = main_font.render('  '.join(a), 1, (28, 28, 28))
    text_rect = string_rendered.get_rect(center=(WIDTH // 2, h))
    screen.blit(string_rendered, text_rect)
    pygame.draw.line(screen, (39, 36, 46), (30, h + 20), (WIDTH - 26, h + 20), 5)
    pygame.draw.line(screen, (39, 36, 46), (390, 30), (390, 582), 5)
    pygame.draw.line(screen, (39, 36, 46), (550, 30), (550, 582), 5)
    pygame.draw.line(screen, (39, 36, 46), (200, 30), (200, 582), 5)
    h += 50
    for txt1 in text:  # считывние строк
        a = ''
        r = 1
        for u in txt1:
            if r == 1:
                t = 8
            elif r == 2:
                t = 11
            elif r == 3:
                t = 9
            else:
                t = 6
            a += u + t * ' '
            r += 1
        if text.index(txt1) < len(text) - 1:
            pygame.draw.line(screen, (39, 36, 46), (30, h + 20), (WIDTH - 26, h + 20), 5)
        string_rendered = main_font.render(a, 1, (28, 28, 28))
        text_rect = string_rendered.get_rect(center=(WIDTH - 530, h))
        screen.blit(string_rendered, text_rect)
        h += 50
    # рисуем линии-разделители
    # pygame.draw.line(screen, (39, 36, 46), (WIDTH // 6 * 4, 0), (WIDTH // 6 * 4, HEIGHT), 10)
    while True:
        return_btn.update(screen)
        return_btn.change_colour(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_btn.click_check(event.pos):
                    main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.flip()
        clock.tick(FPS)


def main_menu():  # главное меню
    pygame.display.set_caption('Escape from Kvantorium')

    text = get_text('Escape from Kvantorium', main_font, (WIDTH // 2, HEIGHT // 10))
    text_shadow = get_text('Escape from Kvantorium', main_font, (WIDTH // 2 + 2, HEIGHT // 10 + 2), (213, 214, 209))

    offscreen = 200

    Border(-offscreen, -offscreen, WIDTH + offscreen, -offscreen)  # - верхний
    Border(-offscreen, HEIGHT + offscreen, WIDTH + offscreen, HEIGHT + offscreen)  # - нижний
    Border(-offscreen, -offscreen, -offscreen, HEIGHT + offscreen)  # | левый
    Border(WIDTH + offscreen, -offscreen, WIDTH + offscreen, HEIGHT + offscreen)  # | правый

    tiles = get_background(bg_image)
    count = 0

    while True:

        count = update_and_draw_backgroud(count, tiles, bg_image)

        all_sprites.draw(screen)
        all_sprites.update()

        draw_text(screen, text_shadow, text)

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
                    leader_board()
                if main_menu_buttons['Настройки'].click_check(event.pos):
                    print('Настрой себя')
                    options()
                if main_menu_buttons['Выход'].click_check(event.pos):
                    terminate()

        for button in main_menu_buttons:
            main_menu_buttons[button].update(screen)
            main_menu_buttons[button].change_colour(pygame.mouse.get_pos())

        pygame.display.flip()
        clock.tick(FPS)


def attempt():  # подсчёт попыток
    base = cur.execute("""SELECT atempts FROM levels
                        WHERE number = ?""", (int(number) + 1,)).fetchall()
    base = base[0][0]
    cur.execute("""UPDATE levels
            SET atempts = ?
            WHERE number = ?""", (int(base) + 1, int(number) + 1)).fetchall()
    con.commit()


# меню уровней
def levels():
    pygame.display.set_caption('Escape from Kvantorium - Выбор уровня')

    text = get_text('Выберите уровень', main_font, (WIDTH // 2, HEIGHT // 10), (213, 214, 209))
    text_shadow = get_text('Выберите уровень', main_font, (WIDTH // 2 - 2, HEIGHT // 10 - 2))
    flag = False
    tiles = get_background(bg_image_character)
    count = 0
    stars = stars_update()
    skip_text = get_text('Смените персонажа для прохождения данного уровня', mini_font,
                         (WIDTH // 2, HEIGHT - 40), (153, 153, 153))
    skip_shadow = get_text('Смените персонажа для прохождения данного уровня', mini_font,
                           (WIDTH // 2 - 2, HEIGHT - 40 - 2), (199, 0, 0))
    while True:

        count = update_and_draw_backgroud(count, tiles, bg_image_character)

        draw_text(screen, text, text_shadow)
        return_btn.update(screen)
        return_btn.change_colour(pygame.mouse.get_pos())

        for button in level_btns:
            button.update(screen)
            button.change_colour(pygame.mouse.get_pos())

        for star_group in stars:
            for star in star_group:
                star.draw(screen)
        if flag:
            draw_text(screen, skip_text, skip_shadow)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_btn.click_check(event.pos):
                    main_menu()
                for button in level_btns:
                    if button.click_check(event.pos):
                        global number
                        print('level' + str(level_btns.index(button) + 1))
                        number = level_btns.index(button)
                        base = cur.execute("""SELECT state FROM levels
                                                WHERE number = ?""", (int(number) + 1,)).fetchall()
                        # проверка разблокирован ли уровень и не взят ли персонаж котрого спасают в этом уровне
                        if base[0][0] == 'разблок' and int(number) + 1 != int(students[selected_character][0]):
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
                            attempt()
                            new_game(level_btns.index(button))
                        if int(number) + 1 == int(students[selected_character][0]):
                            flag = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.flip()
        clock.tick(FPS)


# меню выбора персонажей
def character_selection(character):
    global selected_character
    pygame.display.set_caption('Escape from Kvantorium - Выбор персонажа')

    # получения списка кнопок
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
    elif students[character][0] != '0':
        base = cur.execute("""SELECT stars FROM levels
                                WHERE number = ?""", (students[character][0],)).fetchall()
        if base[0][0] == '0':
            buttons.append(btn_lock)
            selected = False
        else:
            buttons.append(select_btn)
    else:
        buttons.append(select_btn)

    name = get_text(character, main_font, (WIDTH // 6 * 5, HEIGHT // 6))  # имя персонажа
    info = full_wrapper([students[character][-1]], 23)  # информация о персонаже
    info_offsets = [25 * i - (12 * len(info)) for i in range(len(info))]  # информация находится в правой нижней части

    person_image = get_image(load_image(f'characters/{character}.png'), 2, 1, 48, 96, 6)

    info_list = [get_text(line, mini_font, (WIDTH // 6 * 5, HEIGHT // 6 * 4 + info_offsets[info.index(line)]))
                 for line in info]

    tiles = get_background(bg_image_character)
    count = 0

    while True:

        count = update_and_draw_backgroud(count, tiles, bg_image_character)
        pygame.draw.rect(screen, pygame.Color('#f6f4fc'), (WIDTH // 6 * 4, 0, WIDTH, HEIGHT))

        # отрисовывание кнопок и другая текстура при наведении
        for btn in buttons:
            btn.update(screen)
            btn.change_colour(pygame.mouse.get_pos())

        # отрисовывание имени персонажа и онформации о нём
        draw_text(screen, name)
        draw_text(screen, *info_list)

        # отрисовываем картинку персонажа
        screen.blit(person_image, person_image.get_rect(center=(WIDTH // 6 * 2, HEIGHT // 2 - HEIGHT * 0.1)))

        # рисуем линии-разделители
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 6 * 4, 0), (WIDTH // 6 * 4, HEIGHT), 10)
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 6 * 4, HEIGHT // 3), (WIDTH, HEIGHT // 3), 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_RETURN]:
                    base = cur.execute("""SELECT stars FROM levels WHERE number = ?""",
                                       (students[character][0],)).fetchall()
                    if not selected and (students[character][0] == '0' or base[0][0] != '0'):
                        selected_character = character
                        cur.execute(f"""UPDATE data
                                        SET character = '{character}'""")
                        con.commit()
                        buttons[-1] = selected_btn
                        selected = True
                if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and left:  # переходим на кнопку a или стрелку влево
                    character_selection(students_lst[students_lst.index(character) - 1])
                if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and right:  # переходим на кнопку d или стрелку вправо
                    character_selection(students_lst[students_lst.index(character) + 1])
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_btn.click_check(event.pos):
                    main_menu()
                if arrow_left_btn.click_check(event.pos) and left:  # стрелка влево
                    character_selection(students_lst[students_lst.index(character) - 1])
                if arrow_right_btn.click_check(event.pos) and right:  # стрелка вправо
                    character_selection(students_lst[students_lst.index(character) + 1])
                if buttons[-1].click_check(event.pos):
                    base = cur.execute("""SELECT stars FROM levels WHERE number = ?""",
                                       (students[character][0],)).fetchall()
                    if not selected and (students[character][0] == '0' or base[0][0] != '0'):
                        selected_character = character
                        cur.execute(f"""UPDATE data
                                        SET character = '{character}'""")
                        con.commit()
                        buttons[-1] = selected_btn
                        selected = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.flip()
        clock.tick(FPS)


def options():
    pygame.display.set_caption('Escape from Kvantorium - Настройки')

    texts = [get_text('Настройки', main_font, (WIDTH // 2, HEIGHT // 10), (213, 214, 209)),
             get_text('Настройки', main_font, (WIDTH // 2 - 2, HEIGHT // 10 - 2), ),
             get_text('WASD для передвижения + ПРОБЕЛ,', mini_font, (WIDTH // 5 * 3,
                                                                     HEIGHT // 6 * 2 - 8), (213, 214, 209)),
             get_text('CTRL + WASD для создания граффити', mini_font, (WIDTH // 5 * 3,
                                                                       HEIGHT // 6 * 2 + 12), (213, 214, 209)),
             get_text('СТРЕЛКИ для передвижения + ПРОБЕЛ,', mini_font, (WIDTH // 5 * 3,
                                                                        HEIGHT // 6 * 4 - 8), (213, 214, 209)),
             get_text('CTRL + СТРЕЛКИ для создания граффити', mini_font, (WIDTH // 5 * 3,
                                                                          HEIGHT // 6 * 4 + 12), (213, 214, 209)),
             get_text('WASD для передвижения + ПРОБЕЛ,', mini_font, (WIDTH // 5 * 3, HEIGHT // 6 * 2 - 10)),
             get_text('CTRL + WASD для создания граффити', mini_font, (WIDTH // 5 * 3, HEIGHT // 6 * 2 + 10)),
             get_text('СТРЕЛКИ для передвижения + ПРОБЕЛ,', mini_font, (WIDTH // 5 * 3,
                                                                        HEIGHT // 6 * 4 - 10)),
             get_text('CTRL + СТРЕЛКИ для создания граффити', mini_font, (WIDTH // 5 * 3,
                                                                          HEIGHT // 6 * 4 + 10))]

    buttons = [return_btn, check_btn_WASD, check_btn_ARROWS]

    tiles = get_background(bg_image_character)
    count = 0
    while True:

        count = update_and_draw_backgroud(count, tiles, bg_image_character)

        draw_rect(screen, (100, 100, 500, 100), (WIDTH // 5 * 3, HEIGHT // 6 * 2))
        draw_rect(screen, (100, 100, 500, 100), (WIDTH // 5 * 3, HEIGHT // 6 * 4))

        draw_text(screen, *texts)

        for button in buttons:
            button.update(screen)
            if buttons.index(button) == 1:
                if (button.is_checked and buttons[2].is_checked) or not button.is_checked:
                    button.change_colour(pygame.mouse.get_pos())
            elif buttons.index(button) == 2:
                if (button.is_checked and buttons[1].is_checked) or not button.is_checked:
                    button.change_colour(pygame.mouse.get_pos())
            else:
                button.change_colour(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_btn.click_check(event.pos):
                    main_menu()
                if check_btn_WASD.click_check(event.pos):
                    if control_settings['WASD'] and control_settings['ARROWS']:
                        control_settings['WASD'] = False
                        check_btn_WASD.uncheck()
                        cur.execute("""UPDATE data
                                       SET control_wasd = 0""")
                    elif not control_settings['WASD']:
                        control_settings['WASD'] = True
                        check_btn_WASD.check()
                        cur.execute("""UPDATE data
                                       SET control_wasd = 1""")
                    con.commit()
                if check_btn_ARROWS.click_check(event.pos):
                    if control_settings['ARROWS'] and control_settings['WASD']:
                        control_settings['ARROWS'] = False
                        check_btn_ARROWS.uncheck()
                        cur.execute("""UPDATE data
                                       SET control_arrows = 0""")
                    elif not control_settings['ARROWS']:
                        control_settings['ARROWS'] = True
                        check_btn_ARROWS.check()
                        cur.execute("""UPDATE data
                                        SET control_arrows = 1""")
                    con.commit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.flip()
        clock.tick(FPS)


def new_game(level_number):
    global number
    all_sprites = pygame.sprite.Group()
    labirint = Labirint(level[level_number]['level_map'], id_texture, 18)
    person = selected_character
    hero = Hero(*level[level_number]['spawn'], person, hero_font, number)

    total_level_width = labirint.width * 32  # Высчитываем фактическую ширину уровня
    total_level_height = labirint.height * 32  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)
    all_sprites.add(labirint.sprites)

    if 'dop_character' in level[level_number]:
        person = level[level_number]['dop_character']
        if level_number == 9:
            character = pygame.sprite.Group()
            for coord in spawn_teachers:
                teacher = Teacher(*coord)
                character.add(teacher)
        else:
            character = Students(*level[level_number]['spawn_dop'], person)
        all_sprites.add(character)
        level_displayer(level_number, labirint, all_sprites, camera, hero, character)
    level_displayer(level_number, labirint, all_sprites, camera, hero)


# отображает уровень
def level_displayer(level_number, labirint, all_sprites, camera, hero, character=None):
    global number
    pygame.display.set_caption(f'Escape from Kvantorium - {level_number + 1} уровень')
    left = right = up = False
    buttons = [restart_btn, pause_btn]
    timer = Timer(WIDTH // 2, HEIGHT * 0.07, mini_font)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    graffiti_list = []
    drawing = False
    draw_new_graffiti = True
    ctrl = False
    h, w = labirint.size()  # размер
    names = [Text(hero.person, hero_font, hero.rect.x, hero.rect.y, (25, 25, 25))]
    print(level_number)
    if character and level_number != 9:
        names.append(Text(character.person, hero_font, hero.rect.x, hero.rect.y, (25, 25, 25)))
    elif character:
        for teacher in character:
            names.append(Text(teacher.person, hero_font, hero.rect.x, hero.rect.y, (25, 25, 25)))
    all_sprites.add(names[:])

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
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    if draw_new_graffiti:
                        draw_new_graffiti = False
                        drawing = True
                        ctrl = True
                        if (keys[pygame.K_w] and control_settings['WASD']) or \
                                (keys[pygame.K_UP] and control_settings['ARROWS']):
                            graffiti_list.append(Graffiti(pygame.mouse.get_pos(), 'UP'))
                        elif (keys[pygame.K_d] and control_settings['WASD']) or \
                                (keys[pygame.K_RIGHT] and control_settings['ARROWS']):
                            graffiti_list.append(Graffiti(pygame.mouse.get_pos(), 'RIGHT'))
                        elif (keys[pygame.K_s] and control_settings['WASD']) or \
                                (keys[pygame.K_DOWN] and control_settings['ARROWS']):
                            graffiti_list.append(Graffiti(pygame.mouse.get_pos(), 'DOWN'))
                        elif (keys[pygame.K_a] and control_settings['WASD']) or \
                                (keys[pygame.K_LEFT] and control_settings['ARROWS']):
                            graffiti_list.append(Graffiti(pygame.mouse.get_pos(), 'LEFT'))
                        else:
                            ctrl = False
                            draw_new_graffiti = True
                            drawing = False
                    if drawing:
                        # pygame.mouse.set_visible(False)
                        if (keys[pygame.K_w] and control_settings['WASD']) or \
                                (keys[pygame.K_UP] and control_settings['ARROWS']):
                            graffiti_list[-1].change_direction('UP')
                        if (keys[pygame.K_d] and control_settings['WASD']) or \
                                (keys[pygame.K_RIGHT] and control_settings['ARROWS']):
                            graffiti_list[-1].change_direction('RIGHT')
                        if (keys[pygame.K_s] and control_settings['WASD']) or \
                                (keys[pygame.K_DOWN] and control_settings['ARROWS']):
                            graffiti_list[-1].change_direction('DOWN')
                        if (keys[pygame.K_a] and control_settings['WASD']) or \
                                (keys[pygame.K_LEFT] and control_settings['ARROWS']):
                            graffiti_list[-1].change_direction('LEFT')
                    if keys[pygame.K_q]:
                        if drawing:
                            ctrl = False
                            graffiti_list = graffiti_list[:-1]
                            draw_new_graffiti = True
                            drawing = False
                if event.key == pygame.K_ESCAPE:
                    pause()
                if ((keys[pygame.K_a] and control_settings['WASD']) or
                        (keys[pygame.K_LEFT] and control_settings['ARROWS'])) and not ctrl:
                    left = True
                if ((keys[pygame.K_d] and control_settings['WASD']) or
                        (keys[pygame.K_RIGHT] and control_settings['ARROWS'])) and not ctrl:
                    right = True
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] and not ctrl:
                    if pygame.key.get_pressed()[pygame.K_SPACE] or (keys[pygame.K_w] and control_settings['WASD']) or \
                            (keys[pygame.K_UP] and control_settings['ARROWS']):
                        up = 2
                elif (keys[pygame.K_SPACE] or (keys[pygame.K_w] and control_settings['WASD']) or
                      (keys[pygame.K_UP] and control_settings['ARROWS'])) and not ctrl:
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
                    attempt()  # добавляем попытку
                    new_game(level_number)
                if pause_btn.click_check(event.pos):
                    left = right = False
                    pause()
                if drawing:
                    ctrl = False
                    draw_new_graffiti = True
                    drawing = False

        if labirint.is_free(hero.get_position()):
            hero.onGround = False

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.move(left, right, up, labirint.platform, character)  # передвижениe
        names[0].move((hero.rect.x + 10, hero.rect.y - 5))
        if len(names) > 1 and level_number != 9:
            names[1].move((character.rect.x + 10, character.rect.y - 5))
        elif len(names) > 1:
            teachers = list(character)
            for j in range(len(teachers)):
                print(teachers[j])
                names[j + 1].move((teachers[j].rect.x + 10, teachers[j].rect.y - 5))
        if drawing:
            graffiti_list[-1].update((hero.get_position()[0] + hero.w // 2, hero.get_position()[1]))
        for e in all_sprites:
            screen.blit(e.image, camera.apply(e))

        for graffiti in graffiti_list:
            screen.blit(graffiti.image, camera.apply(graffiti))

        if character:
            if isinstance(character, Students):
                character.move(hero.coords_list, hero.xvel)
                screen.blit(character.image, camera.apply(character))
            else:
                for teacher in character:
                    screen.blit(teacher.image, camera.apply(teacher))
                    if pygame.sprite.collide_rect(hero, teacher):
                        game_over(level_number)
                    teacher.move(labirint)

        timer.draw(screen)
        hero.draw(screen, camera)

        for button in buttons:
            button.update(screen)
            button.change_colour(pygame.mouse.get_pos())

        if level[number]['one'] <= timer.get_time():
            game_over(level_number, 'Время кончилось')
        if str(number) in '1468' and character.exit(h, w):  # проверка пройден ли уровень с персонажем
            hero.exit(h, w, False)
            timer.pauses()
            end(timer.get_time())
        elif str(number) in '1468' and hero.exit(h, w) and not character.exit(h, w):
            hero.exit(h, w, False)
        elif hero.exit(h, w) and str(number) in '023579':  # если игрок дошел до выхода
            timer.pauses()
            end(timer.get_time())
        pygame.display.flip()  # обновляем экран
        clock.tick(FPS)


# пауза в уровне
def pause():
    pygame.display.set_caption(f'Escape from Kvantorium - пауза')
    buttons = [home_btn, resume_btn]

    while True:  # игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # возвращаемся в игру
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.click_check(event.pos):
                    return  # возвращаемся в игру
                if home_btn.click_check(event.pos):
                    main_menu()  # выходим из игры, переходим в главное меню

        # окошно в центре окна с двумя кнопками: выход и продолжить
        pygame.draw.rect(screen, pygame.Color('grey'), (WIDTH // 4, HEIGHT // 3, WIDTH // 4 * 2, HEIGHT // 3))
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 4, HEIGHT // 3), (WIDTH // 4 * 3, HEIGHT // 3), 10)
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 4, HEIGHT // 3 * 2), (WIDTH // 4 * 3, HEIGHT // 3 * 2), 10)
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 4, HEIGHT // 3), (WIDTH // 4, HEIGHT // 3 * 2), 10)
        pygame.draw.line(screen, (39, 36, 46), (WIDTH // 4 * 3, HEIGHT // 3), (WIDTH // 4 * 3, HEIGHT // 3 * 2), 10)
        for button in buttons:
            button.update(screen)
            button.change_colour(pygame.mouse.get_pos())

        pygame.display.flip()
        clock.tick(FPS)


def game_over(level_number, reason='Вас поймали'):  # проигрыш
    pygame.display.set_caption(f'Escape from Kvantorium - Game Over')  # изменение названия окна

    game_text = big_font.render('Game', 1, (28, 28, 28))  # создаём текст для отрисовки
    game_text_shadow = big_font.render('Game', 1, (213, 214, 209))  # создаём тень текста для отрисовки
    over_text = big_font.render('Over', 1, (28, 28, 28))
    over_text_shadow = big_font.render('Over', 1, (213, 214, 209))
    reason_text = main_font.render(reason, 1, (28, 28, 28))
    reason_text_shadow = main_font.render(reason, 1, (213, 214, 209))

    tiles_left = tiles_right = get_background(bg_image_game_over)
    walls_collided = False

    count = 0

    while True:
        screen.fill((0, 0, 0))  # закрашиваем фон чёрным

        if count < WIDTH // 2:
            count += 7
        else:
            count = WIDTH // 2
            walls_collided = True

        # отрисовываем задний план, движущийся с двух сторон
        draw_game_over_background(tiles_left, WIDTH - count, bg_image_game_over)
        draw_game_over_background(tiles_right, -WIDTH + count, bg_image_game_over)

        screen.blit(game_text_shadow, game_text.get_rect(center=(-WIDTH // 7 + count + 2, HEIGHT // 7 + 2)))
        screen.blit(over_text_shadow, game_text.get_rect(center=(WIDTH + WIDTH // 7 - count + 2, HEIGHT // 7 + 2)))
        screen.blit(game_text, game_text.get_rect(center=(-WIDTH // 7 + count, HEIGHT // 7)))
        screen.blit(over_text, game_text.get_rect(center=(WIDTH + WIDTH // 7 - count, HEIGHT // 7)))

        if walls_collided:
            screen.blit(reason_text_shadow, game_text.get_rect(center=(WIDTH // 2 + 2 - 25, HEIGHT // 7 * 2 + 2)))
            screen.blit(reason_text, game_text.get_rect(center=(WIDTH // 2 - 25, HEIGHT // 7 * 2)))
            home_btn.update(screen)
            home_btn.change_colour(pygame.mouse.get_pos())
            resume_btn.update(screen)
            resume_btn.change_colour(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                if event.key == pygame.K_RETURN:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.click_check(event.pos) and walls_collided:
                    new_game(level_number)
                    attempt()
                if home_btn.click_check(event.pos) and walls_collided:
                    main_menu()

        pygame.display.flip()
        clock.tick(FPS)


def end(time):  # окончание уровня победой
    global number
    pygame.display.set_caption('Escape from Kvantorium - Победа')
    text = 'ПОБЕДА'
    string_rendered = main_font.render(text, 1, (28, 28, 28))
    string_rendered_shadow = main_font.render(text, 1, (1, 1, 1))
    text_rect = string_rendered.get_rect(center=(WIDTH // 2, HEIGHT // 10))
    screen.blit(string_rendered, text_rect)
    seconds = '0' + str(time % 60) if time % 60 < 10 else str(time % 60)
    minutes = '0' + str(time // 60) if time // 60 < 10 else str(time // 60)
    text1 = 'YOUR TIME: ' + minutes + ':' + seconds
    string_rendern = main_font.render(text1, 1, (28, 28, 28))
    string_rendern_shadow = main_font.render(text1, 1, (1, 1, 1))
    text_rect1 = string_rendern.get_rect(center=(WIDTH // 2, 175))
    screen.blit(string_rendern, text_rect1)
    print(text1)
    tiles = get_background(bg_image_character)
    count = 0
    stars1 = []
    if time <= level[number]['three']:  # выставление звёзд
        stars1.append([Stars(star_active, 'left', 480, 300),
                       Stars(star_active, 'right', 480, 300),
                       Stars(star_active, 'middle', 480, 300)])
        sp = 3
    elif level[number]['two'] >= time > level[number]['three']:
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
            WHERE number = ?""", (int(number) + 1,)).fetchall()
    con.commit()
    if sp > int(base[0][0]):  # изменение количества звезд
        sp1 = base
        sp1[0] = tuple(str(sp))
        print(sp1)
        cur.execute("""UPDATE levels
        SET stars = ?
        WHERE number = ?""", (sp, int(number) + 1)).fetchall()
        con.commit()
        cur.execute("""UPDATE levels  
                SET state = 'разблок'
                WHERE number = ?""", (str(int(number) + 2),)).fetchall()
        con.commit()  # разблокировка следующего уровня
        stars_update()
        level_btns[int(number) + 1] = Button(WIDTH // 6 * 5 if ((int(number) + 2) % 5) == 0 else
                                             WIDTH // 6 * ((int(number) + 2) % 5), HEIGHT // 3
                                             if (int(number) + 2) < 6 else HEIGHT // 3 * 2,
                                             load_image(f'pictures/{int(number) + 2}.png'),
                                             load_image(f'pictures/{int(number) + 2}_.png'), None, WIDTH // 240)
    alpha, direction = 0, 2
    skip_text = mini_font.render('Нажмите ЛЮБУЮ клавишу, чтобы перейти к выбору уровня',
                                 True, (0, 0, 0))
    base = cur.execute("""SELECT time FROM levels
                WHERE number = ?""", (int(number) + 1,)).fetchall()
    base1 = int(base[0][0].split(':')[0])
    base2 = int(base[0][0].split(':')[1])
    if base1 * 60 + base2 > time or base1 * 60 + base2 == 0:  # изменение времени
        cur.execute("""UPDATE levels
                SET time = ?
                WHERE number = ?""", (minutes + ':' + seconds, int(number) + 1)).fetchall()
        con.commit()
    skip_text.set_alpha(alpha)
    while True:
        count = update_and_draw_backgroud(count, tiles, bg_image_character)
        alpha += direction
        if alpha <= 0:
            direction = 4
        elif alpha >= 255:
            direction = -4
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


if __name__ == '__main__':
    main_menu()
