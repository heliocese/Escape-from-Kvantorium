students = {
    'Никита': 'Успевает делать все задания в Лицее. Как именно это ему это удаётся никто не знает. Возможно освоил '
              'знания тайм менеджмента, ну, или же не спит ночами',
    'Ангелина': 'На втором занятии уже всех знала по именам. Коммуникабельная, в общем.  Однажды смогла договориться '
                'с муравьями, правда, не понятно, что больше помогло в переговорах: дихлофос или ее красноречие',
    'Коля': '',
    'Настя': '',
    'Алиса': 'При нашей просьбе написать шуточное описание, она написала резюме:        '
             ' "Спокойна, сдерженна, ценю любые мнения;       И весела довольна, да умна"',
    'Ярик': 'Меняет цвет волос как светофор',
    'Саша': 'Умудрился вылететь из Яндекс лицея до первого дедлайна',
    'Влад': 'Ушел с лицея со словами "Чего-то у меня не получается с python, буду учить java"',
    'Ваня': 'На начало второго года не знал половины группы. Не смог пройти первый уровень с '
            'проектом, больше в Кванториуме его никто не видел. (разработчики сделали ему выпрямление, не удивляйтесь) ',
    'Илья': 'Самый маленький член группы',
    'Максим': 'Он не смог ничего придумать, написав: "Мне лень - подойдёт как описание?"'
}

students_lst = list(students.keys())

level = {0: {'level_map': 'level1.tmx', 'spawn': (780, 445)},
         1: {'level_map': 'level2.tmx', 'spawn': (50, 260), 'dop_character': 'Ярослав', 'spawn_dop': ('x', 'y')},
         2: {'level_map': 'level3.tmx', 'spawn': (40, 800)},
         3: {'level_map': 'level4.tmx', 'spawn': (30, 155)},
         4: {'level_map': 'level5.tmx', 'spawn': (40, 1250), 'dop_character': 'Саша', 'spawn_dop': ('x', 'y')},
         5: {'level_map': 'level6.tmx', 'spawn': (20, 255)},
         6: {'level_map': 'level7.tmx', 'spawn': (175, 65), 'dop_character': 'Влад', 'spawn_dop': ('x', 'y')},
         7: {'level_map': 'level8.tmx', 'spawn': (40, 1000)},
         8: {'level_map': 'level9.tmx', 'spawn': (40, 270), 'dop_character': 'Ваня', 'spawn_dop': ('x', 'y')},
         9: {'level_map': 'level10.tmx', 'spawn': (180, 60)}}


def get_animation(person):
    data = 'data/characters/animation/'

    ANIMATION_DELAY = 80  # скорость смены кадров
    ANIMATION_RIGHT = [(data + person + '_rr1.png'), (data + person + '_rr2.png'), (data + person + '_rr3.png'),
                       (data + person + '_rr4.png')]
    ANIMATION_LEFT = [(data + person + '_rl1.png'), (data + person + '_rl2.png'), (data + person + '_rl3.png'),
                      (data + person + '_rl4.png')]
    ANIMATION_JUMP_LEFT = [(data + person + '_rl1.png', 80)]
    ANIMATION_JUMP_RIGHT = [(data + person + '_rr1.png', 80)]
    ANIMATION = [(data + person + '_0.png', 80)]
    return ANIMATION_DELAY, ANIMATION_RIGHT, ANIMATION_LEFT, ANIMATION_JUMP_RIGHT, ANIMATION_JUMP_LEFT, ANIMATION