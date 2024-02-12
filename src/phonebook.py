from pydantic import BaseModel, Field, ValidationError
from tinydb import TinyDB, Query
from tinydb.queries import QueryLike

NAME_PATTERN = "^[А-Я][а-я]*$"
PERSONAL_PHONE_NUMBER_PATTERN = "^\d{11}$"
WORK_PHONE_NUMBER_PATTERN = PERSONAL_PHONE_NUMBER_PATTERN


class Phonebook:
    def __init__(self, file_path: str = "phonebook.json") -> None:
        self.__contacts: TinyDB = TinyDB(file_path)

    def get_all_contacts(self):
        return self.__contacts.all()

    def add_contact(self, first_name: str, last_name: str, patronymic: str, organization: str, office_number: str,
                    personal_number: str) -> dict:
        """Добавляет контакт в базу данных.

        Args:
            first_name: Имя. Начинается с заглавной буквы, содержит только кириллицу. Аргумент не может быть больше
                одного слова. Пример: "Иван".
            last_name: Фамилия. Начинается с заглавной буквы, содержит только кириллицу. Аргумент не может быть больше
                одного слова. Пример: "Иванов".
            patronymic: Отчество. Начинается с заглавной буквы, содержит только кириллицу. Аргумент не может быть больше
                одного слова. Пример: "Иванович".
            organization: Название организации.
            office_number: Рабочий номер. Пример: "89876543210".
            personal_number: Рабочий номер. Пример: "89876543210".

        Returns:
            Словарь, содержащий ключи "success", "message", и, если контакт успешно добавлен, ключ "id". Параметр
            "success" принимает значение True, если запись добавлена, иначе False. Параметр "message" передает
            информацию о результате функции. Параметр "id" возвращает id добавленной записи. Примеры:
            {"success": True, "message": "Контакт успешно создан!", "id": 3}
            {"success": False, "message": "Контакт с таким личным номером уже создан"}

        """
        try:
            if not self.__contacts.contains(Query().personal_number == personal_number):
                contact: Phonebook.__Contact = self.__Contact(
                    first_name=first_name, last_name=last_name, patronymic=patronymic, organization=organization,
                    office_number=office_number, personal_number=personal_number
                )
                result: int = self.__contacts.insert(contact.model_dump())
                return {"success": True, "message": "Контакт успешно создан!", "id": result}
            else:
                return {"success": False, "message": "Контакт с таким личным номером уже создан."}
        except ValidationError:
            return {"success": False, "message": "Переданы некорректные данные."}

    def get_contacts(self, **kwargs) -> list:
        """Поиск списка контактов.

        Args:
            **kwargs: Переменные, по которым будет происходить поиск. Поиск может происходить по следующим
                параметрам: first_name, last_name, patronymic, organization, office_number, personal_number.

        Returns:
            Список контактов, удовлетворяющих условиям поиска. Например:
            [
             {'first_name': 'Иван', 'last_name': 'Иванов', 'patronymic': 'Иванович', 'organization': 'Название 1',
              'office_number': '81111111111', 'personal_number': '82222222222'},
             {'first_name': 'Петр', 'last_name': 'Петров', 'patronymic': 'Петрович', 'organization': 'Название 2',
              'office_number': '83333333333', 'personal_number': '84444444444'}
            ]
        """
        if not kwargs:
            return self.get_all_contacts()

        search_query: QueryLike = self.__make_query(**kwargs)

        if search_query:
            contacts: list = self.__contacts.search(search_query)
            return contacts
        return []

    def delete_contact(self, personal_number: str) -> dict:
        """Удаление контакта.

        Удаление контакта в том случае, если контакт существует в единственном числе.

        Args:
            personal_number: персональный номер телефона контакта. Используется как уникальный ключ.

        Returns:
            Словарь, содержащий ключи "success" и "message". Параметр "success" принимает значение True, если запись
            удалена, иначе False. Параметр "message" передает информацию о результате функции. Примеры:
            {"success": True, "message": "Контакт успешно удален!"}
            {"success": False, "message": "Контакта не существует."}
        """
        if self.__contacts.contains(Query().personal_number == personal_number):
            self.__contacts.remove(Query().personal_number == personal_number)
            return {"success": True, "message": "Контакт успешно удален!"}
        return {"success": False, "message": "Контакта не существует."}

    def update_contact(self, personal_num: str, **kwargs) -> dict:
        """Обновление контакта по персональному номеру телефона.

        Args:
            personal_num: Персональный номер телефона контакта, который будет обновлен.
            **kwargs: Параметры, которые нужно обновить в контакте. Могут включать first_name, last_name,
                     patronymic, organization, office_number и другие поля контакта.

        Returns:
            Словарь, содержащий ключ "success" и "message". Параметр "success" принимает значение True, если контакт
            успешно обновлен, иначе False. Параметр "message" передает информацию о результате функции.
        """
        if self.__contacts.contains(Query().personal_number == personal_num):
            self.__contacts.update(kwargs, Query().personal_number == personal_num)
            return {"success": True, "message": "Контакт успешно обновлен!"}
        else:
            return {"success": False, "message": "Контакт не найден."}

    def close_db(self):
        self.__contacts.close()

    @staticmethod
    def __make_query(**kwargs) -> QueryLike | None:
        """Составление QueryLike объекта для поиска по базе данных.

        Args:
            **kwargs: параметры, по которым будет производиться поиск.

        Returns:
            QueryLike объект для поиска, если запрашиваемый объект существует, иначе None.
        """
        query: Query = Query()
        search_query = None
        for key, value in kwargs.items():
            if search_query is None:
                search_query = (query[key] == value)
            else:
                search_query &= (query[key] == value)
        return search_query

    class __Contact(BaseModel):
        """Класс для валидации информации о контакте."""
        first_name: str = Field(pattern=NAME_PATTERN)
        last_name: str = Field(pattern=NAME_PATTERN)
        patronymic: str = Field(pattern=NAME_PATTERN)
        organization: str
        office_number: str = Field(pattern=WORK_PHONE_NUMBER_PATTERN)
        personal_number: str = Field(pattern=PERSONAL_PHONE_NUMBER_PATTERN)
