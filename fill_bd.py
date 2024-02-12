"""Файл для генерации тестовой базы данных"""

from tinydb import TinyDB
import random

CONTACTS_COUNT = 100


def generate_number():
    return random.randint(10000000000, 99999999999)


first_names: list = ["Майкл", "Джимм", "Дуайт", "Пэм"]
last_names: list = ["Скотт", "Халперт", "Шрутт", "Бисли"]
patronymics: list = ["Иванович", "Петрович", "Николаевич"]
organizations: list = ["Dunder Mifflin", "Facebook", "Пятёрочка"]

db = TinyDB('phonebook.json')
personal_numbers = set()

for _ in range(CONTACTS_COUNT):
    while True:
        personal_number = generate_number()
        if personal_number not in personal_numbers:
            personal_numbers.add(personal_number)
            break
    office_number = generate_number()

    record = {
        'first_name': random.choice(first_names),
        'last_name': random.choice(last_names),
        'patronymic': random.choice(patronymics),
        'organization': random.choice(organizations),
        'office_number': str(office_number),
        'personal_number': str(personal_number)
    }

    db.insert(record)
