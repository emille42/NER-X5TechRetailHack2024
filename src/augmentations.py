"""
Набор функций для аугментаций датасета
"""


import random
from faker import Faker

random.seed(2024*5)

fake = Faker("ru_RU", seed=2024*5)

# read data parsed from open sources
with open("../src/tech_companies.txt", encoding="utf-8") as f:
    tech_companies = f.read().split("\n")

# read data parsed from open sources (wikipedia)
with open("../src/tech_companies_usa.txt", encoding="utf-8") as f:
    tech_companies_us = f.read().split("\n")

tech_companies_list = tech_companies + tech_companies_us

entity_list = [ "NAME",  "NAME_EMPLOYEE", "PERCENT",  "MAIL", "LINK",  "NUM",  "DATE", "TELEPHONE",  "ACRONYM",  "ORG", "TECH" ]

def do_with_probability(probability=0.5):
    return random.random() < probability

def remove_rand_word(current_tokens):
    words = current_tokens.split(" ")
    if len(words) == 1:
        return current_tokens

    words.pop(random.randint(0, len(words) - 1))

    return " ".join(words)

def create_rand_date():
    if do_with_probability():
        formats = [ "%d.%m.%Y","%d-%m-%Y", "%d/%m/%Y", \
               "%d.%m.%y","%d-%m-%y", "%d/%m/%y"]

        return fake.date_between("-54y", "+75y").strftime(random.choice(formats))
    else:
        day = str(random.randint(1,31))
        name = fake.month_name()

        if do_with_probability():
            name = name.lower()

        if name[-1] == "ь" or name[-1] == "й":
            name = name[:-1] + "я"
        elif name[-1] == "т":
            name = name + "а"

        date = f"{day} {name}"
        if do_with_probability():
            year = str(random.randint(1975, 2099))
            date = f"{date} {year}"
            if do_with_probability():
                if do_with_probability():
                    date = f"{date} г."
                else:
                    date = f"{date} года"
        return date

def create_rand_name(employee=False):
    rand_name = ""

    if do_with_probability():
        prefix = fake.prefix_male()
        last_name = fake.last_name_male()
        name = fake.first_name_male()
        middle_name = fake.middle_name_male()
    else:
        prefix = fake.prefix_female()
        last_name = fake.last_name_female()
        name = fake.first_name_female()
        middle_name = fake.middle_name_female()

    if do_with_probability():
        if do_with_probability():
            rand_name = f"{last_name} {name[0]} {middle_name[0]}"
        else:
            rand_name = f"{last_name} {name[0]}. {middle_name[0]}."
    else:
        if do_with_probability():
            rand_name = f"{last_name} {name} {middle_name}"
        else:
            rand_name = f"{name} {middle_name}"
            if do_with_probability():
                rand_name = f"{name} {last_name}"
    
    if not employee:
        if do_with_probability(0.03):
            rand_name = f"{prefix} {rand_name}"
    else:
        level = ["старший", "младший", "главный", "ответственный"]

        jobs = ["бухгалтер", "менеджер", "руководитель отдела", "эйчар", "HR", \
                "начальник отдела", "администратор", "аналитик", "разработчик", \
                "инженер", "инженер-программист", "секретарь", "агент", \
                "системный администратор", "модератор форума", "программист", "тестировщик", \
                "специалист по информационной безопасности", "системный аналитик", "гейм-дизайнер", \
                "тимлид", "QA-инженер", "директор", "project manager", "product manager", "sales manager", \
                "представитель", "руководитель", "ML инженер", "data scientist", "дата сайентист", \
                "специалист по глубокому обучению", "machine learning инженер", "deep learning инженер", "специалист" \
                "сисадмин", "devops", "девопс", "UX дизайнер", "UI дизайнер", "front end разработчик", "back end разработчик", \
                "архитектор", "SEO", "СЕО", "сеошник", "специалист по машинному обучению", "team lead", \
                "менеджер проекта", "продакт менеджер", "проджекет менеджер", "продавец", "кассир"]
        
        position_level = random.choice(level)
        job_position = random.choice(jobs)

        if do_with_probability(0.3):
            job_position = f"{position_level} {job_position}"
        return rand_name, job_position

    return rand_name


def create_rand_percent():
    if do_with_probability():
        number = round(random.random()*100, 2)
    else:
        number = random.randint(0, 100)

    percents = ["%", " %", "%", "%" ," процента", " процентов", " процент"]

    percent = random.choice(percents)
    number = f"{number}{percent}"

    return number

def create_rand_company():
    if do_with_probability():
        company = fake.company()
    else:
        company = fake.large_company()

    if do_with_probability():
        return f"{fake.company_prefix()} {company}"

    return company

def create_rand_acronym():

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if do_with_probability(0.3):
        letters = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ"

    acronym = ""
    for _ in range(random.randint(3,5)):
        acronym  += random.choice(letters)

    return acronym

def create_new_entity_value(label, tokens, augmented_tokens_list, new_labels_list):
    if label == "O":
        tokens = remove_rand_word(tokens)
        if do_with_probability(0.05):
            tokens = tokens[::-1]

    elif label == "NAME":
        tokens = create_rand_name()

    elif label == "NAME_EMPLOYEE":
        tokens, job_position = create_rand_name(employee=True)
        augmented_tokens_list.append(job_position)
        new_labels_list.append("O")

    elif label == "PERCENT":
        tokens = create_rand_percent()

    elif label == "MAIL":
        tokens = fake.free_email()

    elif label == "LINK":
        tokens = fake.url()

    elif label == "NUM":
        tokens = random.randint(0, 100_000)

    elif label == "DATE":
        tokens = create_rand_date()

    elif label == "TELEPHONE":
        tokens = fake.phone_number()

    elif label == "ACRONYM":
        tokens = create_rand_acronym()

    elif label == "ORG":
        tokens = create_rand_company()

    elif label == "TECH":
        tokens = random.choice(tech_companies_list)


    return tokens, label

def create_random_entity(tokens, augmented_tokens_list, new_labels_list):
    label = random.choice(entity_list)

    return create_new_entity_value(label, tokens, augmented_tokens_list, new_labels_list)


def make_augmentations(data, labels):

    aug_types = ["replace_entity","replace_entity", "replace_entity","replace_entity" , "replace_entity", \
                "replace_entity", "replace_entity", "random_replace", "random_replace", "no_aug"]

    augmented_data = []
    augmented_labels = []
    for tokens, tokens_labels in zip(data, labels):
        augmented_tokens = []
        new_labels = []
        for current_tokens, current_label in zip(tokens, tokens_labels):
            aug = random.choice(aug_types)
            if aug == "replace_entity":
                current_tokens, current_label = create_new_entity_value(current_label, current_tokens, augmented_tokens, new_labels)
            elif aug == "random_replace":

                current_tokens, current_label = create_random_entity(current_tokens, augmented_tokens, new_labels)
            elif aug == "no_aug":
                pass

            augmented_tokens.append(str(current_tokens))
            new_labels.append(current_label)

           
        augmented_data.append(augmented_tokens)
        augmented_labels.append(new_labels)

    return augmented_data, augmented_labels