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
            'проектом, больше в Кванториуме его никто не видел. (разработчики сделали ему выпрямление, не удивляйтесь) '
}

students_lst = list(students.keys())

level = {0: {'level_map': 'level1.tmx', 'spawn': ('x', 'y')},
         1: {'level_map': 'level2.tmx', 'spawn': ('x', 'y'), 'dop_character': 'Ярослав.png', 'spawn_dop': ('x', 'y')},
         2: {'level_map': 'level3.tmx', 'spawn': ('x', 'y')},
         3: {'level_map': 'level4.tmx', 'spawn': ('x', 'y')},
         4: {'level_map': 'level5.tmx', 'spawn': ('x', 'y'), 'dop_character': 'Саша.png', 'spawn_dop': ('x', 'y')},
         5: {'level_map': 'level6.tmx', 'spawn': ('x', 'y')},
         6: {'level_map': 'level7.tmx', 'spawn': ('x', 'y'), 'dop_character': 'Влад.png', 'spawn_dop': ('x', 'y')},
         7: {'level_map': 'level8.tmx', 'spawn': ('x', 'y')},
         8: {'level_map': 'level9.tmx', 'spawn': ('x', 'y'), 'dop_character': 'Ваня.png', 'spawn_dop': ('x', 'y')},
         9: {'level_map': 'level10.tmx', 'spawn': ('x', 'y')}}