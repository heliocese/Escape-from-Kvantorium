import pyganim

# 0 - персонаж открыт или номер уровня в котором спасают данного персонажа
# информация о персонаже
students = {
    'Никита': ['0', 'Успевает делать все задания в Лицее. '
                    'Как именно это ему это удаётся никто не знает. Возможно освоил знания тайм менеджмента, ну, '
                    'или же не спит ночами'],
    'Ангелина': ['0', 'На втором занятии уже всех знала по именам. Коммуникабельная, в общем.  Однажды '
                      'смогла договориться '
                      'с муравьями, правда, не понятно, что больше помогло в переговорах: дихлофос или ее красноречие'],
    'Коля': ['0', 'Обычный мальчик, живущий самой обычной жизнью'],
    'Настя': ['0', 'Испугалась, что Ангелина на самом деле обиделась, когда она с ней не поздоровалась'],
    'Алиса': ['0', 'При нашей просьбе написать шуточное описание, она написала резюме:        '
                   ' "Спокойна, сдерженна, ценю любые мнения;       И весела довольна, да умна"'],
    'Ярик': ['2', 'Меняет цвет волос как светофор'],
    'Саша': ['5', 'Умудрился вылететь из Яндекс.Лицея до первого дедлайна'],
    'Влад': ['7', 'Ушел с лицея со словами "Чего-то у меня не получается с python, буду учить java"'],
    'Ваня': ['8', 'На начало второго года не знал половины группы. Не смог пройти первый уровень с '
                  'проектом, больше в Кванториуме его никто не видел. (разработчики '
                  'сделали ему выпрямление, не удивляйтесь)'],
    'Илья': ['0', 'Самый маленький член группы'],
    'Максим': ['0', 'Он не смог ничего придумать, написав: "Мне лень - подойдёт как описание?"']
}

# список студентов
students_lst = list(students.keys())

# номер уровня, карта, спавн игрока, кол-во звезд, если уровень спасене то спавн второго персонажа
level = {0: {'level_map': 'level1.tmx', 'spawn': (780, 445), 'three': 12, 'two': 24, 'one': 30},
         1: {'level_map': 'level2.tmx', 'spawn': (50, 240), 'dop_character': 'Ярик',
             'spawn_dop': (665, 150), 'three': 24, 'two': 35, 'one': 43},
         2: {'level_map': 'level3.tmx', 'spawn': (85, 728), 'three': 20, 'two': 30, 'one': 40},
         3: {'level_map': 'level4.tmx', 'spawn': (30, 155), 'three': 28, 'two': 35, 'one': 43},
         4: {'level_map': 'level5.tmx', 'spawn': (40, 1250), 'dop_character': 'Саша',
             'spawn_dop': (47, 440), 'three': 55, 'two': 65, 'one': 75},
         5: {'level_map': 'level6.tmx', 'spawn': (20, 255), 'three': 65, 'two': 75, 'one': 90},
         6: {'level_map': 'level7.tmx', 'spawn': (175, 65), 'dop_character': 'Влад',
             'spawn_dop': (327, 1400), 'three': 53, 'two': 68, 'one': 74},
         7: {'level_map': 'level8.tmx', 'spawn': (40, 1021), 'three': 63, 'two': 78, 'one': 90},
         8: {'level_map': 'level9.tmx', 'spawn': (40, 270), 'dop_character': 'Ваня',
             'spawn_dop': (1286, 1300), 'three': 110, 'two': 125, 'one': 135},
         9: {'level_map': 'level10.tmx', 'spawn': (180, 60), 'dop_character': 'Иван',
             'spawn_dop': (576, 40), 'three': 93, 'two': 120, 'one': 240}}

spawn_teachers = [(275, 150), (1591, 534), (2496, 1014), (1345, 1014), (1394, 1590), (856, 1974)]


# анимация персонажей
def get_animation(person, scale=(19, 40)):
    data = 'data/characters/animation/'

    delay = 80  # скорость смены кадров
    right = [(data + person + '_rr1.png'), (data + person + '_rr2.png'), (data + person + '_rr3.png'),
             (data + person + '_rr4.png')]
    left = [(data + person + '_rl1.png'), (data + person + '_rl2.png'), (data + person + '_rl3.png'),
            (data + person + '_rl4.png')]
    jump_left = [(data + person + '_rl1.png', 80)]
    jump_right = [(data + person + '_rr1.png', 80)]
    stay = [(data + person + '_0.png', 80)]
    anim = []
    # Анимация движения вправо
    for a in right:
        anim.append((a, delay))
    anim_right = pyganim.PygAnimation(anim)
    anim_right.scale(scale)
    anim_right.play()
    #Анимация движения влево
    anim = []
    for a in left:
        anim.append((a, delay))
    anim_left = pyganim.PygAnimation(anim)
    anim_left.scale(scale)
    anim_left.play()
    # стоим
    anim_stay = pyganim.PygAnimation(stay)
    anim_stay.play()
    anim_stay.scale(scale)
    # Анимация прыжка влево
    anim_jump_left = pyganim.PygAnimation(jump_left)
    anim_jump_left.scale(scale)
    anim_jump_left.play()
    # Анимация прыжка вправо
    anim_jump_right = pyganim.PygAnimation(jump_right)
    anim_jump_right.scale(scale)
    anim_jump_right.play()

    return delay, anim_right, anim_left, anim_jump_right, anim_jump_left, anim_stay
