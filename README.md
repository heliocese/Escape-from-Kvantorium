
# Тема: Создание игры на pygame.
# Escape from Kvantorium


Целью проекта является создание игры с помощью библиотеки pygame.
В данном проекте реализована игра в стиле платформер-лабиринт, в которой присутствуют упоминания реально существующих людей и учебного заведения “[Кванториум](https://kvantorium.ru/)”.

### Сюжет

Сюжет игры заключается в побеге из вышеупомянутого учебного заведения, на некоторых уровнях которого игрок должен спасти своих потерявшихся одногруппников. На последнем уровне надо сбежать от преподавателя Ивана Дмитриевича.

### Дизайн

Дизайн был сделан наподобие детского Технопарка.

### Разделы меню

В меню игры есть несколько разделов: играть, выбор персонажа, статистика, настройки и выход. 

- При выборе опции “Играть” пользователь переходит в меню уровней. У каждого уровня есть показатель завершённости, выполненный в трёх звёздах. Уровни разблокируются по мере прохождения предыдущих.

- Во вкладке “Выбор персонажа” пользователь может выбрать за кого он будет играть. Не все персонажи доступны изначально, некоторых надо открыть при спасении на определённых уровнях. Персонаж, которого спасли на уровне, не может играть на этом уровне.

- В статистике присутствует данные по всем уровням: разблокирован или заблокирован уровень, количество попыток, лучшее время прохождения и количество звёзд за уровень.

- В настройках есть возможность поменять клавиши управления. Изначально передвижение осуществляется на стрелочки, а создание граффити при зажатии Ctrl + нужная стрелка. Можно изменить на WASD. Прыжок осуществляется при нажатии на пробел/W/стрелку наверх(зависит от выбранных настроек). Высокий прыжок активируется при зажатии Shift и соответствующей клавиши.

- При нажатии на выход игра закрывается.

### ТЗ:
1. Сделать дизайн для уровней, меню, настроек и тд.
2. Меню
   - Сделать переход к уровням ✅
   - Сделать вкладку с выбором персонажа ✅
   - Выводить статистику по уровням 
   - Дать возможность пользователю менять клавиши управления в настройках ✅
   - сделать кнопку выхода ✅
3. Сделать разные виды уровней
   - Просто нахождение выхода из лабиринта ✅
   - Спасение другого персонажа ✅
   - Побег от преподавателя(последний уровень)
4. Во вкладке с выбором персонажа давать пользователю, соответственно, выбирать персонажа
   - придумать описание к персонажам ✅
   - создать спрайты персонажей ✅
5. Вывод статистики по всем уровням
   - кол-во попыток
   - лучшее время прохождения
   - кол-во звезд
   - состояние уровня(заблокировано/разблокировано)
6. В настройках дать выбор управления персонажем при прохождении уровней(клавиши) ✅
7. Возможные дополнения
   - музыка
   - столкновение с предметами декора
   - имя персонажа над головой во время прохождения игры
   - граффити на стенах
   - мини-карта уровня

### При реализации проекта использованы:
1. Библиотеки
   - pygame
   - Pyganim
   - PyTMX
2. Приложение для создания карт для уровней и тайлов Tiled
3. [Сайт](https://cazwolf.itch.io/pixel-charagen) для генерации спрайтов персонажей 
