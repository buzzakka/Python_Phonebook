from src.phonebook import Phonebook
from unittest import TestCase
import os


class TestPhonebook(TestCase):
    @classmethod
    def setUpClass(cls):
        # Путь к тестовой базе данных
        cls.db_path = "tests/test_bd.json"

        cls.user_data: dict = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "patronymic": "Иванович",
            "organization": "Effective Mobile",
            "office_number": "89991575656",
            "personal_number": "89991575656",
        }

    def setUp(self):
        self.phonebook: Phonebook = Phonebook(self.db_path)

    def tearDown(self):
        self.phonebook.close_db()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_add_correct_contact(self):
        """Добавление корректного контакта"""
        length: int = len(self.phonebook.get_all_contacts())
        result = self.phonebook.add_contact(**self.user_data)
        assert (len(self.phonebook.get_all_contacts()) == length + 1)
        assert (result["success"] is True)
        assert (result["message"] == "Контакт успешно создан!")
        assert (result["id"] == 1)
        assert (self.phonebook.get_all_contacts()[0] == self.user_data)

    def test_add_two_correct_contact(self):
        """Добавление двух корректных контактов"""
        length: int = len(self.phonebook.get_all_contacts())
        self.phonebook.add_contact(**self.user_data)
        second_contact: dict = self.user_data.copy()
        second_contact["first_name"] = "Петр"
        second_contact["personal_number"] = "89171575656"
        result = self.phonebook.add_contact(**second_contact)
        assert (len(self.phonebook.get_all_contacts()) == length + 2)
        assert (result["success"] is True)
        assert (result["message"] == "Контакт успешно создан!")
        assert (result["id"] == 2)
        assert (self.phonebook.get_all_contacts() == [self.user_data, second_contact])

    def test_add_contact_which_already_exists(self):
        """Добавление существующего контакта"""
        length: int = len(self.phonebook.get_all_contacts())
        self.phonebook.add_contact(**self.user_data)
        result = self.phonebook.add_contact(**self.user_data)
        assert (result["success"] is False)
        assert (result["message"] == "Контакт с таким личным номером уже создан.")
        assert (len(self.phonebook.get_all_contacts()) == length + 1)

    def test_add_contact_with_incorrect_values(self):
        """Добавление контакта с некорректными данными"""
        incorrect_data: dict = {
            "first_name": ["имя", "Имя имя", "Name"],
            "last_name": ["фамилия", "Фам илия", "Lastname"],
            "patronymic": ["отчество", "Отч ество", "patronymic"],
            "office_number": ["8999155555", "899915555511", "номер"],
            "personal_number": ["8999155555", "899915555511", "номер"]
        }
        length: int = len(self.phonebook.get_all_contacts())
        for key, value in incorrect_data.items():
            for elem in value:
                temp_user = self.user_data.copy()
                temp_user[f"{key}"] = elem
                result = self.phonebook.add_contact(**temp_user)
                assert (result["success"] is False)
                assert (result["message"] == "Переданы некорректные данные.")
                assert (len(self.phonebook.get_all_contacts()) == length)

    def get_all_contacts(self):
        """Получение всех номеров"""
        self.phonebook.add_contact(**self.user_data)
        second_contact: dict = self.user_data.copy()
        second_contact["personal_number"] = "89991001495"
        result: dict = self.phonebook.get_all_contacts()
        assert result == [self.user_data, second_contact]

    def test_get_contact_by_first_name(self):
        """Поиск контактов по имени"""
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(first_name=self.user_data["first_name"])
        assert contacts == [self.user_data]

    def test_get_contact_by_last_name(self):
        """Поиск контактов по фамилии"""
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(last_name=self.user_data["last_name"])
        assert contacts == [self.user_data]

    def test_get_contact_by_patronymic(self):
        """Поиск контактов по отчеству"""
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(patronymic=self.user_data["patronymic"])
        assert contacts == [self.user_data]

    def test_get_contact_by_organization(self):
        """Поиск контактов по организации"""
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(organization=self.user_data["organization"])
        assert contacts == [self.user_data]

    def test_get_contact_by_office_number(self):
        """Поиск контактов по офисному номеру телефона"""
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(office_number=self.user_data["office_number"])
        assert contacts == [self.user_data]

    def test_get_contact_by_personal_number(self):
        """Поиск контактов по личному офисному номеру"""
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(personal_number=self.user_data["personal_number"])
        assert contacts == [self.user_data]

    def test_get_contact_with_incorrect_first_name(self):
        """Поиск контактов по некорректному имени"""
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(first_name="Петр")
        assert contacts == []

    def test_get_contact_with_incorrect_last_name(self):
        """Поиск контактов по некорректной фамилии"""
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(last_name="Петров")
        assert contacts == []

    def test_get_contact_with_incorrect_patronymic(self):
        """Поиск контактов по некорректному отчеству"""
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(patronymic="Петрович")
        assert contacts == []

    def test_get_contact_with_incorrect_organization(self):
        """Поиск контактов по некорректной организации"""
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(organization="Тест")
        assert contacts == []

    def test_get_contact_with_incorrect_office_number(self):
        """Поиск контактов по некорректному офисному номеру телефона"""
        incorrect_data: dict = {
            "personal_number": "89999999999"
        }
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(office_number="89999999999")
        assert contacts == []

    def test_get_contact_with_incorrect_personal_number(self):
        """Поиск контактов по некорректному личному номеру телефона"""
        self.phonebook.add_contact(**self.user_data)
        contacts: list = self.phonebook.get_contacts(personal_number="89999999999")
        assert contacts == []

    def test_delete_existing_contact(self):
        """Удалени существующего контакта"""
        self.phonebook.add_contact(**self.user_data)
        length: int = len(self.phonebook.get_contacts())
        result = self.phonebook.delete_contact(self.user_data["personal_number"])
        assert len(self.phonebook.get_contacts()) == length - 1
        assert result == {"success": True, "message": "Контакт успешно удален!"}

    def test_delete_not_existing_contact(self):
        """Удалени несуществующего контакта"""
        length: int = len(self.phonebook.get_contacts())
        result = self.phonebook.delete_contact("89999999999")
        assert len(self.phonebook.get_contacts()) == length
        assert result == {"success": False, "message": "Контакта не существует."}

    def test_edit_contact(self):
        """Обновление контакта"""
        self.phonebook.add_contact(**self.user_data)
        new_contact: dict = {
            "first_name": "Петр",
            "last_name": "Петров",
            "patronymic": "Петрович",
            "organization": "Microsoft",
            "office_number": "81111111111",
            "personal_number": "82222222222",
        }
        result: dict = self.phonebook.update_contact(self.user_data["personal_number"], **new_contact)
        assert self.phonebook.get_all_contacts()[0] == new_contact
        assert result == {"success": True, "message": "Контакт успешно обновлен!"}

    def test_edit_not_existent_contact(self):
        """Обновление контакта"""
        self.phonebook.add_contact(**self.user_data)
        result: dict = self.phonebook.update_contact("81110200202", **self.user_data)
        assert result == {"success": False, "message": "Контакт не найден."}
