from art import tprint
from tabulate import tabulate
from phonebook import Phonebook


class View:
    phonebook = Phonebook()

    @staticmethod
    def draw_main_menu():
        """Отрисовка главного меню"""
        View.clear_console()
        tprint("PhoneBook")
        print("Главное меню:")
        print("1. Вывод всех контактов.")
        print("2. Найти контакт.")
        print("3. Добавить новый контакт.")
        print("4. Изменить контакт.")
        print("5. Удалить контакт.")
        print("0. Выход.\n")

    def render_main_menu(self) -> None:
        while True:
            self.draw_main_menu()
            choice: str = input("Выберите пункт: ")
            match choice:
                case "1":
                    self.render_all_contacts_page()
                case "2":
                    print(2)
                case "3":
                    pass
                case "0":
                    break

    def print_paginated_contacts(self, contacts: list) -> None:
        paginated_contacts = self.get_paginated_list(contacts)
        max_page = len(paginated_contacts)
        current_page = 1
        while True:
            self.clear_console()
            print("Все контакты\n")
            self.print_contacts_table(paginated_contacts[current_page - 1])
            print(f"\nСтр. {current_page}/{max_page}")

            if max_page == 1:
                print("Введите 0 для выхода.")
            else:
                print(
                    f"Введите номер страницы [{1}-{max_page}], или -/+ для перехода между страницами. Введите 0 для"
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
    def print_contacts_table(contacts: list) -> None:
        header: list = ["id", "Имя", "Фамилия", "Отчество", "Организация", "Телефон рабочий", "Телефон личный"]
        table = [[contact["id"], contact["first_name"], contact["last_name"], contact["patronymic"], contact["organization"],
                 contact["office_number"], contact["personal_number"]] for contact in contacts]
        print(tabulate(table, headers=header))

    def render_all_contacts_page(self) -> None:
        contacts: list = self.get_all_contacts()
        self.print_paginated_contacts(contacts)

    def get_all_contacts(self) -> list:
        contacts: list = self.phonebook.get_contacts()
        sorted_contacts: list = self.get_sorted_list(contacts)
        return sorted_contacts

    @staticmethod
    def get_sorted_list(contacts: list) -> list:
        sorted_contacts: list = sorted(
            contacts, key=lambda x: (x["last_name"], x["first_name"], x["patronymic"], x["organization"])
        )
        sorted_contacts_with_index = [{"id": i + 1, **contact} for i, contact in enumerate(sorted_contacts)]
        return sorted_contacts_with_index

    @staticmethod
    def get_paginated_list(contacts: list, num_at_page: int = 2) -> list:
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
            try:
                choice_int = int(choice)
                if min_value <= choice_int <= max_value or choice_int == 0:
                    return choice_int
                raise ValueError()
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
        view.render_main_menu()


if __name__ == "__main__":
    View.run_app()
