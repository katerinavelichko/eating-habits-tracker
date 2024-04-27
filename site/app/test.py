import json
import pandas as pd
import requests


def make_df_for_model(current_user, QuestionsSleep):
    user_id = current_user.get_id()
    user_answers = QuestionsSleep.query.filter_by(user_id=user_id).first()
    if user_answers:
        user_answers_dict = {
            'tofu': user_answers.tofu,
            'processed_meat': user_answers.processed_meat,
            'play_sport': user_answers.play_sport,
            'eat_weekend': user_answers.eat_weekend,
            'sleep_night': user_answers.sleep_night,
            'sugary_drinks': user_answers.sugary_drinks,
            'cows_milk': user_answers.cows_milk,
            'fresh_cheeses': user_answers.fresh_cheeses,
            'miss_meals': user_answers.miss_meals,
            'vegetable_drinks': user_answers.vegetable_drinks,
            'eat_fast': user_answers.eat_fast,
            'cooked_vegetables': user_answers.cooked_vegetables,
            'low_fat_yogurt': user_answers.low_fat_yogurt,
            'wake_up_eat_night': user_answers.wake_up_eat_night,
            'hungry_during_day': user_answers.hungry_during_day,
            'nuts': user_answers.nuts,
            'fish': user_answers.fish,
            'fruits': user_answers.fruits,
            'eggs': user_answers.eggs,
            'whole_grains_food': user_answers.whole_grains_food,
            'eat_uncontrollably': user_answers.eat_uncontrollably,
            'alcoholic_beverages': user_answers.alcoholic_beverages,
            'meat': user_answers.meat,
            'sex': user_answers.sex
        }
    else:
        user_answers_dict = {}
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
        'Утром': 'In the morning',
        'Вечером': 'In the evening',
        'Днем': 'In the afternoon',
        'До обеда': 'Before lunch',
        "После обеда": 'After lunch',
        "Перед ужином": 'Before Dinner',
        "После ужина": 'After Dinner',
        "Я всегда голоден": "I'm always hungry",
        "Да, завтрак": 'Yes, breakfast',
        "Да, обед": 'Yes, lunch',
        "Да, ужин": 'Yes, dinner',
        "Да, из-за нехватки времени": "I have no time",
        "У меня нет перекусов в течение дня": "Yes for craving",
        "Сладости": 'Sweets',
        "Всегда": "I'm always hungry",
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

    json_data = json.dumps(user_answers_dict, ensure_ascii=False)
    data_dict = json.loads(json_data)
    translated_data = {key: eng_answers[value] if value in eng_answers else value for key, value in data_dict.items()}

    food_dict = {}
    food = ['Tofu', 'Processed Meat (es prosciutto)',
            "Cow's milk", 'Fresh cheeses',
            'Cooked vegetables', 'Low-fat white yogurt',
            'Nuts', 'Fish', 'Fruits', 'Eggs',
            'Whole grains food',
            'Meat']
    food_db = ['tofu', 'processed_meat', 'cows_milk', 'fresh_cheeses', 'cooked_vegetables', 'low_fat_yogurt', 'nuts',
               'fish', 'fruits', 'eggs', 'whole_grains_food', 'meat']
    for i in range(len(food_db)):
        food_dict[food_db[i]] = food[i]
    res = {'alcoholic_beverages': 'How many times do you consume alcoholic beverages in a week?',
           'eat_uncontrollably': "Do you happen to eat uncontrollably even if you're not hungry",
           'eat_weekend': "Do you eat differently at the weekend",
           'hungry_during_day': "When are you hungry during the day?",
           'miss_meals': 'Do you ever miss meals?',
           'play_sport': "Do you play a sport (at least 5 hours/week)?",
           'sugary_drinks': 'How many sugary drinks do you consume per day?',
           'wake_up_eat_night': 'Do you wake up to eat at night?',
           'sex': 'SEX', 'tofu': 'Tofu',
           'processed_meat': 'Processed Meat (es prosciutto)',
           'cows_milk': "Cow's milk",
           'fresh_cheeses': 'Fresh cheeses',
           'cooked_vegetables': 'Cooked vegetables',
           'low_fat_yogurt': 'Low-fat white yogurt',
           'nuts': 'Nuts',
           'fish': 'Fish',
           'fruits': 'Fruits',
           'eggs': 'Eggs',
           'whole_grains_food': 'Whole grains food',
           'meat': 'Meat'}
    answer_dict = {}

    for key, value in translated_data.items():
        if key in food_db:
            new_key_no = food_dict[key] + "_No"
            new_key_sometimes = food_dict[key] + "_Sometimes"
            new_key_yes = food_dict[key] + "_Yes"

            answer_dict[new_key_no] = 1 if value == "No" else 0
            answer_dict[new_key_sometimes] = 1 if value == "Sometimes" else 0
            answer_dict[new_key_yes] = 1 if value == "Yes" else 0
        elif key == 'eat_weekend':
            new_key_no = res[key] + "_No"
            new_key_elaborate = res[key] + "_I cook more elaborate"
            new_key_restaurants = res[key] + "_Yes, I eat at restaurants"
            new_key_home = res[key] + "_Yes, I eat more at home"

            answer_dict[new_key_no] = 1 if value == "No" else 0
            answer_dict[new_key_elaborate] = 1 if value == "I cook more elaborate" else 0
            answer_dict[new_key_restaurants] = 1 if value == "Yes, I eat at restaurants" else 0
            answer_dict[new_key_home] = 1 if value == "Yes, I eat more at home" else 0

        elif key == 'alcoholic_beverages':
            new_key_alcohol = res[key]

            answer_dict[new_key_alcohol] = value

        elif key == 'miss_meals':
            new_key_no = res[key] + "_No"
            new_key_yes = res[key] + "_Yes"
            new_key_breakfast = res[key] + "_Yes, breakfast"
            new_key_dinner = res[key] + "_Yes, dinner"
            new_key_lunch = res[key] + "_Yes, lunch"

            answer_dict[new_key_no] = 1 if value == "No" else 0
            answer_dict[new_key_breakfast] = 1 if value == "Yes, breakfast" else 0
            answer_dict[new_key_yes] = 1 if value == "Yes" else 0
            answer_dict[new_key_dinner] = 1 if value == "Yes, dinner" else 0
            answer_dict[new_key_lunch] = 1 if value == "Yes, lunch" else 0

        elif key == 'eat_uncontrollably':
            new_key_everyday = res[key] + "_Every day"
            new_key_infreq = res[key] + "_Infrequent (1/month)"
            new_key_never = res[key] + "_Never"
            new_key_often = res[key] + "_Often (>1/week)"

            answer_dict[new_key_everyday] = 1 if value == "Every day" else 0
            answer_dict[new_key_infreq] = 1 if value == "Infrequent (1/month)" else 0
            answer_dict[new_key_never] = 1 if value == "Never" else 0
            answer_dict[new_key_often] = 1 if value == "Often (>1/week)" else 0

        elif key == 'play_sport':
            new_key_no = res[key] + "_No"
            new_key_yes = res[key] + "_Yes"

            answer_dict[new_key_no] = 1 if value == "No" else 0
            answer_dict[new_key_yes] = 1 if value == "Yes" else 0

        elif key == 'sugary_drinks':
            new_key_sugary = res[key]

            answer_dict[new_key_sugary] = value

        elif key == 'hungry_during_day':
            new_key_everyday = res[key] + "_Every day"
            new_key_yes = res[key] + "_Yes"
            new_key_breakfast = res[key] + "_Yes, breakfast"
            new_key_dinner = res[key] + "_Yes, dinner"
            new_key_lunch = res[key] + "_Yes, lunch"

            answer_dict[new_key_everyday] = 1 if value == "Every day" else 0
            answer_dict[new_key_breakfast] = 1 if value == "Yes, breakfast" else 0
            answer_dict[new_key_yes] = 1 if value == "Yes" else 0
            answer_dict[new_key_dinner] = 1 if value == "Yes, dinner" else 0
            answer_dict[new_key_lunch] = 1 if value == "Yes, lunch" else 0

        elif key == 'sex':
            new_key_m = res[key] + '_M'
            new_key_f = res[key] + '_F'

            answer_dict[new_key_m] = 1 if value == 'M' else 0
            answer_dict[new_key_f] = 1 if value == 'F' else 0

        elif key == 'wake_up_eat_night':
            new_key_everyday = res[key] + '_Every_day'
            new_key_infrequent = res[key] + '_Infrequent (1/month)'
            new_key_never = res[key] + '_Never'
            new_key_often = res[key] + '_Often (>1/week)'

            answer_dict[new_key_everyday] = 1 if value == "Every day" else 0
            answer_dict[new_key_often] = 1 if value == "Often" else 0
            answer_dict[new_key_never] = 1 if value == "Never" else 0
            answer_dict[new_key_infrequent] = 1 if value == "Infrequent" else 0

    answer_dict["Tofu_Don't know"] = 0

    df = pd.DataFrame(answer_dict, index=[0]).reset_index()

    df = df.drop('index', axis=1)

    df.columns = [col.replace(' ', '_').replace('?', '').replace('%', '').replace('(', '').replace(')', '').replace(',',
                                                                                                                    '').replace(
        ':', '').replace('{', '').replace('}', '') for col in df.columns]

    df = df.rename(columns={
        'When_are_you_hungry_during_the_day_Every_day': "When_are_you_hungry_during_the_day_I'm_always_hungry",
        'When_are_you_hungry_during_the_day_Yes': "When_are_you_hungry_during_the_day_afternoon+evening",
        'When_are_you_hungry_during_the_day_Yes_breakfast': "When_are_you_hungry_during_the_day_In_the_morning",
        'When_are_you_hungry_during_the_day_Yes_dinner': "When_are_you_hungry_during_the_day_In_the_evening",
        'When_are_you_hungry_during_the_day_Yes_lunch': "When_are_you_hungry_during_the_day_In_the_afternoon"
    })

    original = (
        "Tofu_Don't_know",
        "Tofu_No",
        "Tofu_Sometimes",
        "Tofu_Yes",
        "Processed_Meat_es_prosciutto_No",
        "Processed_Meat_es_prosciutto_Sometimes",
        "Processed_Meat_es_prosciutto_Yes",
        "SEX_F",
        "SEX_M",
        "Do_you_play_a_sport_at_least_5_hours/week_No",
        "Do_you_play_a_sport_at_least_5_hours/week_Yes",
        "Do_you_eat_differently_at_the_weekend_I_cook_more_elaborate",
        "Do_you_eat_differently_at_the_weekend_No",
        "Do_you_eat_differently_at_the_weekend_Yes_I_eat_at_restaurants",
        "Do_you_eat_differently_at_the_weekend_Yes_I_eat_more_at_home",
        "Cow's_milk_No",
        "Cow's_milk_Sometimes",
        "Cow's_milk_Yes",
        "Fresh_cheeses_No",
        "Fresh_cheeses_Sometimes",
        "Fresh_cheeses_Yes",
        "Do_you_ever_miss_meals_No",
        "Do_you_ever_miss_meals_Yes",
        "Do_you_ever_miss_meals_Yes_breakfast",
        "Do_you_ever_miss_meals_Yes_dinner",
        "Do_you_ever_miss_meals_Yes_lunch",
        "Cooked_vegetables_No",
        "Cooked_vegetables_Sometimes",
        "Cooked_vegetables_Yes",
        "Low-fat_white_yogurt_No",
        "Low-fat_white_yogurt_Sometimes",
        "Low-fat_white_yogurt_Yes",
        "Do_you_wake_up_to_eat_at_night_Every_day",
        "Do_you_wake_up_to_eat_at_night_Infrequent_1/month",
        "Do_you_wake_up_to_eat_at_night_Never",
        "Do_you_wake_up_to_eat_at_night_Often_>1/week",
        "When_are_you_hungry_during_the_day_I'm_always_hungry",
        "When_are_you_hungry_during_the_day_In_the_afternoon",
        "When_are_you_hungry_during_the_day_In_the_evening",
        "When_are_you_hungry_during_the_day_In_the_morning",
        "When_are_you_hungry_during_the_day_afternoon+evening",
        "Nuts_No",
        "Nuts_Sometimes",
        "Nuts_Yes",
        "Fish_No",
        "Fish_Sometimes",
        "Fish_Yes",
        "Fruits_No",
        "Fruits_Sometimes",
        "Fruits_Yes",
        "Eggs_No",
        "Eggs_Sometimes",
        "Eggs_Yes",
        "Whole_grains_food_No",
        "Whole_grains_food_Sometimes",
        "Whole_grains_food_Yes",
        "Do_you_happen_to_eat_uncontrollably_even_if_you're_not_hungry_Every_day",
        "Do_you_happen_to_eat_uncontrollably_even_if_you're_not_hungry_Infrequent_1/month",
        "Do_you_happen_to_eat_uncontrollably_even_if_you're_not_hungry_Never",
        "Do_you_happen_to_eat_uncontrollably_even_if_you're_not_hungry_Often_>1/week",
        "Meat_No",
        "Meat_Sometimes",
        "Meat_Yes",
        "How_many_sugary_drinks_do_you_consume_per_day",
        "How_many_times_do_you_consume_alcoholic_beverages_in_a_week"
    )
    dictionary = df.to_dict(orient='records')
    tmp_dict = {}
    for col in original:
        tmp_dict[col] = [d[col] for d in dictionary][0]

    final_dict = tmp_dict.copy()
    cnt1 = 0
    features = []

    # итерируемся по всему массиву, за исключением последних 2-х, для них есть своя проверка
    for i in original[:-2]:
        if len(features) >= 3 or cnt1 >= len(tmp_dict.keys()):
            break

        if int(tmp_dict['How_many_sugary_drinks_do_you_consume_per_day']) > 2:
            features.append('How_many_sugary_drinks_do_you_consume_per_day')
            tmp_dict['How_many_sugary_drinks_do_you_consume_per_day'] = 0
        elif int(tmp_dict['How_many_times_do_you_consume_alcoholic_beverages_in_a_week']) > 0:
            features.append('How_many_times_do_you_consume_alcoholic_beverages_in_a_week')
            tmp_dict['How_many_times_do_you_consume_alcoholic_beverages_in_a_week'] = 0
        elif int(tmp_dict[i]) == 1:
            features.append(i)
            tmp_dict[i] = 0
        cnt1 += 1
    final_df = pd.DataFrame(final_dict, index=[0]).reset_index()

    final_df = final_df.drop('index', axis=1)

    return [final_df, features]


def translator(user_products):
    API_KEY = config["yandextranslate"]["api"]
    text = [key for key in user_products.keys()]
    grams = [val for val in user_products.values()]
    res, translated_text = [], []

    source_lang = 'ru'
    target_lang = 'en'
    format_type = 'PLAIN_TEXT'

    url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
    headers = {'Authorization': f'Api-Key {API_KEY}', 'Content-Type': 'application/json'}

    data = {
        'sourceLanguageCode': source_lang,
        'targetLanguageCode': target_lang,
        'format': format_type,
        'texts': [text]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        translated_text = [response.json()['translations'][i]['text'] for i in range(len(text))]
    else:
        print("Error:", response.status_code)
        print("Response content:", response.text)

    for i, j in zip(translated_text, grams):
        res.append({'product_name': i, 'grams': j})

    return res
