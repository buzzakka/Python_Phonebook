from art import tprint
from phonebook import Phonebook


class View:
    phonebook = Phonebook()

    def print_main_menu(self) -> None:
        """Отрисовка меню"""
        View.clear_console()
        tprint("PhoneBook")
        print("Главное меню:")
        print("1. Вывод всех контактов.")
        print("2. Найти контакт.")
        print("3. Добавить новый контакт.")
        print("4. Изменить контакт.")
        print("5. Удалить контакт.")
        print("0. Выход.\n")
        self.get_users_menu_choice(1, 5)
        self.get_all_contacts()

    def print_paginated_contacts(self, paginated_list: list) -> None:
        counter: int = 1
        while

    def get_all_contacts(self) -> None:
        contacts: list = self.phonebook.get_contacts()
        sorted_contacts: list = self.get_sorted_list(contacts)
        paginated_list: list = self.get_paginated_list(sorted_contacts)
        return paginated_list

    @staticmethod
    def get_sorted_list(contacts: list) -> list:
        sorted_contacts: list = sorted(
            contacts, key=lambda x: (x["last_name"], x["first_name"], x["patronymic"], x["organization"])
        )
        return sorted_contacts

    @staticmethod
    def get_paginated_list(contacts: list, num_at_page: int = 1) -> list:
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
    def get_users_menu_choice(min_value: int, max_value: int):
        """Выбор пункта меню"""
        while True:
            choice = input("Выберите вариант: ")
            if choice == "0":
                exit()
            try:
                choice_int = int(choice)
                if not min_value <= choice_int <= max_value:
                    raise ValueError()
                return choice_int
            except ValueError:
                print("Выберите корректное значение.")

    @staticmethod
    def clear_console():
        """Отчистка консоли"""
        print("\033[H\033[J")

    @staticmethod
    def run_app():
        """Запуск приложения"""
        view: View = View()
        view.print_main_menu()


if __name__ == "__main__":
    View.run_app()
