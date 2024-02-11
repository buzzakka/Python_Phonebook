from art import tprint
from phonebook import Phonebook


class View:
    phonebook = Phonebook()

    @staticmethod
    def print_main_menu():
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
        choice: int = View.get_users_menu_choice(1, 5)

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
        View.print_main_menu()


if __name__ == "__main__":
    View.run_app()
