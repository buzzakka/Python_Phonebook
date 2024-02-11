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

    def test_add_contact_which_already_exists(self):
        """Добавление существующего контакта"""
        length: int = len(self.phonebook.get_all_contacts())
        self.phonebook.add_contact(**self.user_data)
        result = self.phonebook.add_contact(**self.user_data)
        assert (result["success"] is False)
        assert (result["message"] == "Контакт с таким личным номером уже создан.")
        assert (len(self.phonebook.get_all_contacts()) == length + 1)

    def test_add_contact_with_incorrect_first_name_1(self):
        """Имя с маленькой буквы"""
        length: int = len(self.phonebook.get_all_contacts())
        temp_user = self.user_data.copy()
        temp_user["first_name"] = "имя"
        result = self.phonebook.add_contact(**temp_user)
        assert (result["success"] is False)
        assert (result["message"] == "Переданы некорректные данные.")
        assert (len(self.phonebook.get_all_contacts()) == length)

    def test_add_contact_with_incorrect_first_name_2(self):
        """Имя в 2 слова"""
        length: int = len(self.phonebook.get_all_contacts())
        temp_user = self.user_data.copy()
        temp_user["first_name"] = "Имя имя"
        result = self.phonebook.add_contact(**temp_user)
        assert (result["success"] is False)
        assert (result["message"] == "Переданы некорректные данные.")
        assert (len(self.phonebook.get_all_contacts()) == length)

    def test_add_contact_with_incorrect_first_name_3(self):
        """Имя не на кириллице"""
        length: int = len(self.phonebook.get_all_contacts())
        temp_user = self.user_data.copy()
        temp_user["first_name"] = "Name"
        result = self.phonebook.add_contact(**temp_user)
        assert (result["success"] is False)
        assert (result["message"] == "Переданы некорректные данные.")
        assert (len(self.phonebook.get_all_contacts()) == length)

    def test_add_contact_with_incorrect_last_name_1(self):
        """Фамилия с маленькой буквы"""
        length: int = len(self.phonebook.get_all_contacts())
        temp_user = self.user_data.copy()
        temp_user["last_name"] = "фамилия"
        result = self.phonebook.add_contact(**temp_user)
        assert (result["success"] is False)
        assert (result["message"] == "Переданы некорректные данные.")
        assert (len(self.phonebook.get_all_contacts()) == length)

    def test_add_contact_with_incorrect_last_name_2(self):
        """Фамилия в 2 слова"""
        length: int = len(self.phonebook.get_all_contacts())
        temp_user = self.user_data.copy()
        temp_user["last_name"] = "Фам илия"
        result = self.phonebook.add_contact(**temp_user)
        assert (result["success"] is False)
        assert (result["message"] == "Переданы некорректные данные.")
        assert (len(self.phonebook.get_all_contacts()) == length)

    def test_add_contact_with_incorrect_last_name_3(self):
        """Фамилия не на кириллице"""
        length: int = len(self.phonebook.get_all_contacts())
        temp_user = self.user_data.copy()
        temp_user["last_name"] = "Lastname"
        result = self.phonebook.add_contact(**temp_user)
        assert (result["success"] is False)
        assert (result["message"] == "Переданы некорректные данные.")
        assert (len(self.phonebook.get_all_contacts()) == length)

    def test_add_contact_with_incorrect_patronymic_1(self):
        """Отчество с маленькой буквы"""
        length: int = len(self.phonebook.get_all_contacts())
        temp_user = self.user_data.copy()
        temp_user["patronymic"] = "отчество"
        result = self.phonebook.add_contact(**temp_user)
        assert (result["success"] is False)
        assert (result["message"] == "Переданы некорректные данные.")
        assert (len(self.phonebook.get_all_contacts()) == length)

    def test_add_contact_with_incorrect_patronymic_2(self):
        """Отчество в 2 слова"""
        length: int = len(self.phonebook.get_all_contacts())
        temp_user = self.user_data.copy()
        temp_user["patronymic"] = "Отч ество"
        result = self.phonebook.add_contact(**temp_user)
        assert (result["success"] is False)
        assert (result["message"] == "Переданы некорректные данные.")
        assert (len(self.phonebook.get_all_contacts()) == length)

    def test_add_contact_with_incorrect_patronymic_3(self):
        """Отчество не на кириллице"""
        length: int = len(self.phonebook.get_all_contacts())
        temp_user = self.user_data.copy()
        temp_user["patronymic"] = "Patronymic"
        result = self.phonebook.add_contact(**temp_user)
        assert (result["success"] is False)
        assert (result["message"] == "Переданы некорректные данные.")
        assert (len(self.phonebook.get_all_contacts()) == length)

