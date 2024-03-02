import csv

# Заводим словарик для перевода всех фраз из нашего датасета
eng_answers = {
    "Да": "Yes",
    "Нет": "No",
    'больше': 'More',
    "Иногда": 'Sometimes',
    "Не знаю": "Don't know",
    "М": 'M',
    "Ж": 'F',
    'Да, я больше ем дома': 'Yes I eat more at home',
    'Да, я ем в ресторанах': 'Yes I eat at restaurants',
    'Я готовлю более изысканно': 'I cook more elaborate',
    'Когда я просыпаюсь': 'When I wake Up',
    'Утром': 'During the morning',
    'Днем': 'In the afternoon',
    'До обеда': 'Before lunch',
    "После обеда": 'After lunch',
    "Перед ужином": 'Before Dinner',
    "После ужина": 'After Dinner',
    "Я всегда голоден": "I'm always hungry",
    "Да, завтрак": 'Yes breakfast',
    "Да, обед": 'Yes lunch',
    "Да, ужин": 'Yes dinner',
    "Да, из-за нехватки времени": "I have no time",
    "У меня нет перекусов в течение дня": "Yes for craving",
    "Сладости": 'Sweets',
    "Фрукты": 'Fruits',
    "овощи": 'vegetables',
    "Орехи": 'Nuts',
    "Бутерброды/сэндвичи": 'Sandwiches',
    "Батончики": 'Bars',
    "хлебцы": 'breads',
    "Каждый день": 'Every day',
    "Часто (больше 1 раза в неделю)": 'Often (>1/week)',
    "Нечасто (около 1-го раза в месяц)": 'Infrequent (1/month)',
    "Никогда": "Never",
    "Хорошо": 'Good',
    "Я с трудом засыпаю": 'I struggle to fall asleep',
    "Я просыпаюсь несколько раз за ночь": 'I wake up several times during the night',
    "Я просыпаюсь намного раньше, чем хотелось бы": 'I wake up a lot sooner than I would like',
    "Часто с кем-то": 'Often Together',
    "Часто в одиночестве": 'Often Alone',
    "В одиночестве во время завтрака": 'Alone at breakfast',
    "В одиночестве во время обеда": 'Alone at lunch',
    "В одиночестве во время ужина": 'Alone at dinner',
    "Начинаю есть больше": "I'm starting to eat more",
    "Начинаю есть меньше": "I'm starting to eat less",
    "Никак не влияет": "Doesn't have any effect",
    "У меня нет стресса": "I have no stress"
}

with open(file='data/Our dataset.csv', mode='r', encoding='utf-8') as file:
    tmp = csv.reader(file)
    cnt = -1
    for row in tmp:
        for el in range(len(row)):
            # проверяем все те колонки, в составе которых есть элементы с запятыми
            if el == 22 or el == 23 or el == 28 or el == 30 or el == 36:
                flag = 1
                cnt = 1 if 'Я всегда голоден' in row[el] else 0

                # здесь идет обработка всех тех неприятных строк, у которых внутри есть запятая
                # если строка без запятых, то тогда просто создаем list fix
                if 'Да' in row[el]:
                    fix = [x.strip(', ') for x in row[el].split('Да, ')][1:]
                    fix[-1] = fix[-1].replace(', Я всегда голоден', '')
                    if cnt:
                        fix.append('Я всегда голоден')
                    flag = 0
                elif "Я просыпаюсь намного раньше, чем хотелось бы" in row[el]:
                    fix = [x.strip() for x in row[el].split(',')][:-1]
                    fix[-1] = "Я просыпаюсь намного раньше, чем хотелось бы"
                else:
                    fix = [x.strip() for x in row[el].split(',')]

                for i in range(len(fix)):
                    if flag and fix[i] in eng_answers.keys():
                        fix[i] = eng_answers[fix[i]]
                    elif not flag:
                        # пытаемся обратиться в словарь по ключу вида "Да" + наше распаршенное обращение
                        # если не получается, значит мы наткнулись на
                        try:
                            fix[i] = eng_answers['Да, ' + fix[i]]
                        except:
                            fix[i] = eng_answers[fix[i]]
                row[el] = '"' + ','.join(fix) + '"'
            elif row[el] in eng_answers.keys():
                row[el] = eng_answers[row[el]]

        # создаем файл
        with open(file='Dataset.csv', mode='a', encoding='utf-8') as file1:
            file1.write(','.join(row) + '\n')
