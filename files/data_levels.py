import pyganim


students = {
    'Никита': 'Успевает делать все задания в Лицее. Как именно это ему это удаётся никто не знает. Возможно освоил '
              'знания тайм менеджмента, ну, или же не спит ночами',
    'Ангелина': 'На втором занятии уже всех знала по именам. Коммуникабельная, в общем.  Однажды смогла договориться '
                'с муравьями, правда, не понятно, что больше помогло в переговорах: дихлофос или ее красноречие',
    'Коля': 'Обычный мальчик, живущий самой обычной жизнью',
    'Настя': 'Испугалась, что Ангелина на самом деле обиделась, когда она с ней не поздоровалась',
    'Алиса': 'При нашей просьбе написать шуточное описание, она написала резюме:        '
             ' "Спокойна, сдерженна, ценю любые мнения;       И весела довольна, да умна"',
    'Ярик': 'Меняет цвет волос как светофор',
    'Саша': 'Умудрился вылететь из Яндекс.Лицея до первого дедлайна',
    'Влад': 'Ушел с лицея со словами "Чего-то у меня не получается с python, буду учить java"',
    'Ваня': 'На начало второго года не знал половины группы. Не смог пройти первый уровень с '
            'проектом, больше в Кванториуме его никто не видел. (разработчики сделали ему выпрямление, не удивляйтесь)',
    'Илья': 'Самый маленький член группы',
    'Максим': 'Он не смог ничего придумать, написав: "Мне лень - подойдёт как описание?"'
}

students_lst = list(students.keys())

level = {0: {'level_map': 'level1.tmx', 'spawn': (780, 445), 'three': 30, 'two': 40, 'one': 50},
         1: {'level_map': 'level2.tmx', 'spawn': (50, 240), 'dop_character': 'Ярик',
             'spawn_dop': (665, 150), 'three': 32, 'two': 50, 'one': 60},
         2: {'level_map': 'level3.tmx', 'spawn': (40, 800), 'three': 15, 'two': 30, 'one': 40},
         3: {'level_map': 'level4.tmx', 'spawn': (30, 155), 'three': 30, 'two': 45, 'one': 60},
         4: {'level_map': 'level5.tmx', 'spawn': (40, 1250), 'dop_character': 'Саша',
             'spawn_dop': (47, 440), 'three': 63, 'two': 70, 'one': 75},
         5: {'level_map': 'level6.tmx', 'spawn': (20, 255), 'three': 60, 'two': 100, 'one': 120},
         6: {'level_map': 'level7.tmx', 'spawn': (175, 65), 'dop_character': 'Влад',
             'spawn_dop': (327, 1400), 'three': 170, 'two': 190, 'one': 220},
         7: {'level_map': 'level8.tmx', 'spawn': (40, 1021), 'three': 130, 'two': 150, 'one': 180},
         8: {'level_map': 'level9.tmx', 'spawn': (40, 270), 'dop_character': 'Ваня',
             'spawn_dop': (1286, 1300), 'three': 420, 'two': 480, 'one': 540},
         9: {'level_map': 'level10.tmx', 'spawn': (180, 60), 'dop_character': 'Иван',
             'spawn_dop': (576, 40), 'three': 160, 'two': 200, 'one': 240}}


def get_animation(person):
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

    for a in right:
        anim.append((a, delay))
    anim_right = pyganim.PygAnimation(anim)
    anim_right.scale((19, 40))
    anim_right.play()
    #        Анимация движения влево
    anim = []
    for a in left:
        anim.append((a, delay))
    anim_left = pyganim.PygAnimation(anim)
    anim_left.scale((19, 40))
    anim_left.play()

    anim_stay = pyganim.PygAnimation(stay)
    anim_stay.play()
    anim_stay.scale((19, 40))

    anim_jump_left = pyganim.PygAnimation(jump_left)
    anim_jump_left.scale((19, 40))
    anim_jump_left.play()

    anim_jump_right = pyganim.PygAnimation(jump_right)
    anim_jump_right.scale((19, 40))
    anim_jump_right.play()

    return delay, anim_right, anim_left, anim_jump_right, anim_jump_left, anim_stay
