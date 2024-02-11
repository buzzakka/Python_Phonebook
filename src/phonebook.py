from pydantic import BaseModel, Field
from tinydb import TinyDB, Query

NAME_PATTERN = "^[А-Я][а-я]*$"
PERSONAL_PHONE_NUMBER_PATTERN = "^\d{11}$"
WORK_PHONE_NUMBER_PATTERN = PERSONAL_PHONE_NUMBER_PATTERN


class Contact(BaseModel):
    first_name: str = Field(pattern=NAME_PATTERN)
    last_name: str = Field(pattern=NAME_PATTERN)
    patronymic: str = Field(pattern=NAME_PATTERN)
    organization: str
    office_number: str = Field(pattern=WORK_PHONE_NUMBER_PATTERN)
    personal_number: str = Field(pattern=PERSONAL_PHONE_NUMBER_PATTERN)


class Phonebook:
    __contacts: TinyDB = TinyDB("phonebook.json")

    def add_contact(self, first_name: str, last_name: str,  patronymic: str, organization: str, office_number: str,
                    personal_number: str) -> int | None:
        """ Добавляет контакт в базу данных.

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
            id объекта, если добавляемый объект не существует, иначе None.
        """

        contact: Contact = Contact(
            first_name=first_name, last_name=last_name, patronymic=patronymic, organization=organization,
            office_number=office_number, personal_number=personal_number
        )
        if contact.dict() not in self.__contacts:
            result: int = self.__contacts.insert(contact.dict())
            return result
        return None

    def get_contact(self, **kwargs) -> list:
        """ Поиск списка контактов.

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
        query: Query = Query()
        search_query = None
        for key, value in kwargs.items():
            if search_query is None:
                search_query = (query[key] == value)
            else:
                search_query &= (query[key] == value)
                print(search_query)

        if search_query:
            contacts: list = self.__contacts.search(search_query)
            return contacts
        return []


data = {
    "first_name": "Марсель",
    "last_name": "Рашитов",
    "patronymic": "Приколистов",
    "organization": "йцуйцу",
    "office_number": "89991575858",
    "personal_number": "89991585858",
}
if __name__ == "__main__":
    p = Phonebook()
    p.add_contact(first_name="Мсарсель", last_name="Привет", patronymic="Ффыв", organization="фысчя", office_number="89991575959", personal_number="89991212222")
    # print(c)
    # p.get_contact(office_number="89991575959")
