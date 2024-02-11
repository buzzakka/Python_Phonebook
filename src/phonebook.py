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

    def add_contact(self, first_name: str, last_name: str,  patronymic: str, organization: str, office_number: str,
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
        except ValidationError as e:
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
            Returns:
            Словарь, содержащий ключи "success" и "message". Параметр "success" принимает значение True, если запись
            удалена, иначе False. Параметр "message" передает информацию о результате функции. Примеры:
            {"success": True, "message": "Контакт успешно удален!"}
            {"success": False, "message": "Такого контакта не существует."}
        """
        search_query: QueryLike = self.__make_query(personal_number=personal_number)

        if search_query:
            self.__contacts.remove(search_query)
            return {"success": True, "message": "Контакт успешно удален!"}
        return {"success": False, "message": "Такого контакта не существует."}

    def update_contact(self, **kwargs) -> bool:
        """Обновление контакта.

        Обновление контакта в том случае, если контакт существует в единственном числе. Если найдено несколько
        вариантов, то возникает ValueError.

        Args:
            **kwargs: параметры обновляемого контакта. Поиск может происходить по следующим параметрам: first_name,
                last_name, patronymic, organization, office_number, personal_number.

        Returns:
            True, если объект был обновлен, иначе False.

        Raises:
            ValueError: Если по заданным параметрам найдено несколько записей.
        """
        search_query: QueryLike = self.__make_query(**kwargs)

        if search_query:
            contacts: list = self.__contacts.search(search_query)
            if len(contacts) == 1:
                self.__contacts.remove(search_query)
                return True
            elif len(contacts) > 1:
                raise ValueError("Несколько объектов для удаления")
        return False

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


data = {
    "first_name": "Артемий",
    "last_name": "Рашитов",
    "patronymic": "Приколистов",
    "organization": "йцуйцу",
    "office_number": "89991575858",
    "personal_number": "89992585818",
}
if __name__ == "__main__":
    p = Phonebook()
    # print(c)
    r = p.add_contact(**data)
    print(r)
    # new_data = data.copy()
    # new_data["first_name"] = "Яков"
    print(sorted(p.get_contacts(), key=lambda x: (x['last_name'], x['first_name'])))
    # c = p.delete_contact(office_number="89991575959", patronymic="Ффыв",)
    # print(c)
    # print(p.get_all_contacts())
