from art import tprint
from tabulate import tabulate
from src.phonebook import Phonebook, NAME_PATTERN, PERSONAL_PHONE_NUMBER_PATTERN, WORK_PHONE_NUMBER_PATTERN
import re

RED_COLOR = "\u001b[31m"
BLUE_COLOR = "\u001b[34m"
GREEN_COLOR = "\u001b[32m"
END_COLOR = "\033[0m"


class View:
    __phonebook: Phonebook = Phonebook()

    @staticmethod
    def draw_logo(logo_text: str = "Phonebook") -> None:
        """Выводит логотип программы.

        Args:
            logo_text: Текст логотипа, стандартное значение Phonebook.
        """
        print(BLUE_COLOR, sep="", end="")
        tprint(logo_text, font="clr8x8")
        print(END_COLOR, sep="", end="")

    @staticmethod
    def draw_main_menus_options():
        """Отрисовка разделов главного меню"""
        print(f"{BLUE_COLOR}Главное меню:{END_COLOR}")
        print("1. Вывод всех контактов.")
        print("2. Найти контакт.")
        print("3. Добавить новый контакт.")
        print("4. Изменить контакт.")
        print("5. Удалить контакт.")
        print("0. Выход.\n")

    def draw_main_menu(self) -> None:
        """Отрисовка главного меню"""
        while True:
            self.clear_console()
            self.draw_logo()
            self.draw_main_menus_options()
            choice: str = input("Выберите пункт [0-5]: ")
            match choice:
                case "1":
                    self.draw_all_contacts_page()
                case "2":
                    self.draw_get_contacts_page()
                case "3":
                    self.draw_add_new_contact()
                case "4":
                    self.draw_update_contact()
                case "5":
                    self.draw_delete_contact()
                case "0":
                    break

    def draw_paginated_contacts(self, contacts: list) -> None:
        """Отрисовка контактов с пагинацией

        Args:
            contacts: Список контактов в формате [{contact_1}, {contact_2}, ...]
        """
        if len(contacts) == 0:
            print(f"{BLUE_COLOR}Все контакты:{END_COLOR}")
            input(f"{RED_COLOR}Список контактов пуст. Нажмите любую клавишу для выхода в меню...{END_COLOR}")
            return

        paginated_contacts: list = self.get_paginated_list(contacts)
        max_page = len(paginated_contacts)
        current_page: int = 1
        while True:
            self.clear_console()
            print(f"{BLUE_COLOR}Все контакты:{END_COLOR}\n")
            self.draw_contacts_table(paginated_contacts[current_page - 1])
            print(f"\nСтр. {current_page}/{max_page}\n")

            if max_page == 1:
                print("Нажмите [0] для выхода.")
            else:
                print(
                    f"[{1}-{max_page}] для перехода к странице, или [-]/[+] для перехода между страницами. [0] для "
                    f"выхода в меню.")

            choice = input("Выберите: ")
            if choice == "-" and current_page > 1:
                current_page -= 1
            elif choice == "+" and current_page < max_page:
                current_page += 1
            elif choice.isdigit() and 1 <= int(choice) <= max_page:
                current_page = int(choice)
            elif choice == "0":
                break

    @staticmethod
    def draw_contacts_table(contacts: list) -> None:
        """Отрисовка контактов в виде таблицы

        Args:
            contacts (list): Список контактов в формате [{contact_1}, {contact_2}, ...]
        """
        header: list = ["id", "Фамилия", "Имя", "Отчество", "Организация", "Телефон рабочий", "Телефон личный"]
        table = [
            [contact["id"], contact["last_name"], contact["first_name"], contact["patronymic"], contact["organization"],
             contact["office_number"], contact["personal_number"]]
            for contact in contacts]
        print(tabulate(table, headers=header))

    def draw_all_contacts_page(self) -> None:
        """Отрисовка раздела со всеми контактами"""
        contacts: list = self.get_contacts_wiht_filtres()
        self.clear_console()
        self.draw_paginated_contacts(contacts)

    def get_contacts_wiht_filtres(self, **kwargs) -> list:
        """Получение контактов с фильтрами в отсортированном виде.

        Если фильтры не указаны, возвращает список всех контактов.

        Args:
            **kwargs (dict): список фильтров

        Returns:
            Отсортированный список в формате [{contact_1}, {contact_2}, ...]
        """
        contacts: list = self.__phonebook.get_contacts(**kwargs)
        sorted_contacts: list = self.get_sorted_list(contacts)
        return sorted_contacts

    def draw_get_contacts_page(self) -> None:
        """Отрисовка раздела с поиском контактов"""
        self.clear_console()
        print(f"{BLUE_COLOR}Поиск контактов.{END_COLOR}\n")
        data: dict = {
            "last_name": input("Введите Фамилию: "),
            "first_name": input("Введите Имя: "),
            "patronymic": input("Введите Отчество: "),
            "organization": input("Введите Организацию: "),
            "office_number": input("Введите Рабочий телефон: "),
            "personal_number": input("Введите Личный телефон: ")
        }
        result_data: dict = {key: value for key, value in data.items() if value}
        contacts: list = self.get_contacts_wiht_filtres(**result_data)
        if len(contacts) == 0:
            input(f"\n{RED_COLOR}Контактов не найдено, нажмите любую клавишу для выхода...{END_COLOR}")
        else:
            self.clear_console()
            print(f"{BLUE_COLOR}Поиск контактов.{END_COLOR}\n")
            self.draw_paginated_contacts(contacts)

    def draw_add_new_contact(self):
        """Добавление нового контакта"""
        self.clear_console()
        data: dict = {
            "first_name": self.get_correct_param(
                "Введите имя. Имя должно содержать только кириллицу и начинаться с заглавной буквы.",
                pattern=NAME_PATTERN
            ),
            "last_name": self.get_correct_param(
                "Введите фамилию. Фамилия должна содержать только кириллицу и начинаться с заглавной буквы.",
                pattern=NAME_PATTERN
            ),
            "patronymic": self.get_correct_param(
                "Введите отчество. Отчество должно содержать только кириллицу и начинаться с заглавной буквы.",
                pattern=NAME_PATTERN
            ),
            "organization": self.get_correct_param(
                "Введите название организации.",
            ),
            "office_number": self.get_correct_param(
                "Введите рабочий номер телефона в формате 89999999999. Номер не должен содержать лишних символов и"
                "должен содержать 11 цифр.",
                pattern=WORK_PHONE_NUMBER_PATTERN
            ),
            "personal_number": self.get_correct_param(
                "Введите личный номер телефона в формате 89999999999. Номер не должен содержать лишних символов и "
                "должен содержать 11 цифр.",
                pattern=PERSONAL_PHONE_NUMBER_PATTERN
            ),
        }
        result = self.__phonebook.add_contact(**data)
        print(result["message"])
        print()
        input("Нажмите любую клавишу чтобы продолжить...")

    def draw_update_contact(self) -> None:
        """Обновление существующего контакта

        Для обновления необходимо ввести номер телефона существующего контакта.
        """
        self.clear_console()
        print("Обновление контакта:")
        personal_number: str = self.get_correct_param(
            "Введите личный номер телефона в формате 89999999999. Номер должен существовать в базе. Номер не"
            "должен содержать лишних символов и должен содержать 11 цифр.",
            pattern=PERSONAL_PHONE_NUMBER_PATTERN)
        contacts: list = self.__phonebook.get_contacts(personal_number=personal_number)
        if contacts:
            self.clear_console()
            print(f"{BLUE_COLOR}Найден следующий контакт:{END_COLOR}\n")
            self.draw_contacts_table(self.get_sorted_list(contacts))
            print()
            contact: dict = contacts[0]
            data: dict = {
                "first_name": self.get_correct_param(
                    "Введите имя. Имя должно содержать только кириллицу и начинаться с заглавной буквы. "
                    "Оставьте поле пустым если хотите оставить текущее значение.",
                    contact["first_name"],
                    NAME_PATTERN
                ),
                "last_name": self.get_correct_param(
                    "Введите фамилию. Фамилия должна содержать только кириллицу и начинаться с заглавной буквы. "
                    "Оставьте поле пустым если хотите оставить текущее значение.",
                    contact["last_name"],
                    NAME_PATTERN
                ),
                "patronymic": self.get_correct_param(
                    "Введите отчество. Отчество должно содержать только кириллицу и начинаться с заглавной буквы. "
                    "Оставьте поле пустым если хотите оставить текущее значение.",
                    contact["patronymic"],
                    NAME_PATTERN
                ),
                "organization": self.get_correct_param(
                    "Введите название организации.",
                    contact["organization"],
                ),
                "office_number": self.get_correct_param(
                    "Введите рабочий номер телефона в формате 89999999999. Номер не должен содержать лишних символов и"
                    "должен содержать 11 цифр. Оставьте поле пустым если хотите оставить текущее значение.",
                    contact["office_number"],
                    WORK_PHONE_NUMBER_PATTERN
                ),
                "personal_number": self.get_correct_param(
                    "Введите личный номер телефона в формате 89999999999. Номер не должен содержать лишних символов и "
                    "должен содержать 11 цифр. Оставьте поле пустым если хотите оставить текущее значение.",
                    contact["personal_number"],
                    PERSONAL_PHONE_NUMBER_PATTERN
                ),
            }
            result: dict = self.__phonebook.update_contact(personal_num=contact["personal_number"], **data)
            if result["success"]:
                print(GREEN_COLOR + result["message"] + END_COLOR)
            else:
                print(RED_COLOR + result["message"] + END_COLOR)
        else:
            print(f"{RED_COLOR}Контакта с таким личным номером не существует.{END_COLOR}")
        print()
        input("Нажмите на любую клавишу чтобы продолжить...")

    def draw_delete_contact(self):
        """Удаление существующего контакта

        Для удаления необходимо ввести номер телефона существующего контакта.
        """
        self.clear_console()
        print(f"{BLUE_COLOR}Удаление контакта:{END_COLOR}")
        personal_number = self.get_correct_param(
            "Введите личный номер телефона в формате 89999999999. Номер должен существовать в базе. Номер не"
            "должен содержать лишних символов и должен содержать 11 цифр.",
            pattern=PERSONAL_PHONE_NUMBER_PATTERN)
        contacts: list = self.__phonebook.get_contacts(personal_number=personal_number)
        if contacts:
            print("Найден следующий контакт:\n")
            self.draw_contacts_table(self.get_sorted_list(contacts))
            print()
            choice = input("Уверены, что хотите удалить контакт? [Да/Нет]: ")
            if choice.lower() == "да":
                result: dict = self.__phonebook.delete_contact(personal_number=personal_number)
                if result["success"]:
                    print(GREEN_COLOR + result["message"] + END_COLOR)
                else:
                    print(RED_COLOR + result["message"] + END_COLOR)
            else:
                print(f"{RED_COLOR}Контакт не был удален.{END_COLOR}")
        else:
            print(f"{RED_COLOR}Контакта с таким личным номером не существует.{END_COLOR}")
        print()
        input("Нажмите на любую клавишу чтобы продолжить...")

    @staticmethod
    def get_correct_param(help_text: str, default_value: str | None = None, pattern: str = "\\w+") -> str:
        """Получение от пользователя корректных параметров.

        Получение от пользователя параметров, которые должны соответствовать шаблону регулярного выражения pattern.
        Если параметр введен неправильно, то у пользователя повторно запросятся данные.

        Args:
            help_text: Текст с подсказкой для параметра. Будете выводится перед input.
            default_value: Дефолтное значение для параметров.
            pattern: Паттерн регулярного выражения, на основании которого будет проводится проверка корректности
                введеынх пользователем данных. Если параметр не введен, то допускается любые названия (кроме пустых
                строк).

        Returns:
             Корректный параметр, соответствующий входному шаблону.
        """
        print(help_text)
        param: str = input("Введите значение: ")
        print()
        if not param and default_value is not None:
            return default_value
        while re.match(pattern, param) is None:
            print(f"{RED_COLOR}Введены некорректные данные. {help_text} {END_COLOR}")
            param: str = input("Введите значение: ")
            print()
        return param

    @staticmethod
    def get_sorted_list(contacts: list) -> list:
        """Получение сортированного списка контактов

        Args:
            contacts (list): список контактов

        Returns:
            Отсортированный список контактов в формате [{contact_1}, {contact_2}, ...]
        """
        sorted_contacts: list = sorted(
            contacts, key=lambda x: (x["last_name"], x["first_name"], x["patronymic"], x["organization"])
        )
        sorted_contacts_with_index = [{"id": i + 1, **contact} for i, contact in enumerate(sorted_contacts)]
        return sorted_contacts_with_index

    @staticmethod
    def get_paginated_list(contacts: list, num_at_page: int = 5) -> list:
        """Получение списка контактов с пагинацией

        Args:
            contacts (list): список контактов в формате [{contact_1}, {contact_2}, ...]
            num_at_page (int): количество контактов на странице, по умолчанию 5

        Returns:
            Список, содержащий списки контактов размером до num_at_page контактов. Пример:
            [[{contact_1}, ..., {contact_5}], [{contact_6}, ..., {contact_7}], ...]
        """
        result: list = []
        counter: int = 0
        current_list: list = []
        for elem in contacts:
            current_list.append(elem)
            counter += 1
            if counter == num_at_page:
                result.append(current_list)
                counter = 0
                current_list = []
        if counter % num_at_page != 0:
            result.append(current_list)
        return result

    @staticmethod
    def clear_console() -> None:
        """Отчистка консоли"""
        print("\033[H\033[J")
