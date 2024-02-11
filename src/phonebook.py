from pydantic import BaseModel, Field
from collections import OrderedDict

NAME_PATTERN = "^[А-Я][а-я]*$"
OWN_PHONE_NUMBER_PATTERN = "^\d{11}$"
WORK_PHONE_NUMBER_PATTERN = OWN_PHONE_NUMBER_PATTERN


class Contact(BaseModel):
    firstname: str = Field(pattern=NAME_PATTERN)
    lastname: str = Field(pattern=NAME_PATTERN)
    patronymic: str = Field(pattern=NAME_PATTERN)
    organization: str
    work_number: str = Field(pattern=WORK_PHONE_NUMBER_PATTERN)
    own_number: str = Field(pattern=OWN_PHONE_NUMBER_PATTERN)

    def __str__(self):
        return f"{self.lastname} {self.firstname} {self.patronymic}"


class Phonebook:
    contacts: set = set()

    def add_contact(self, **kwargs):
        contact = Contact(**kwargs)
        self.contacts.add(contact)
        print(self.contacts)


data = {
    'firstname': 'Марсель',
    'lastname': 'Рашитов',
    'patronymic': 'Приколистов',
    'organization': 'йцуйцу',
    'work_number': '89991575858',
    'own_number': '89991585858',
}
if __name__ == "__main__":
    p = Phonebook()
    p.add_contact(firstname='Марсель', lastname='Привет', patronymic='Ффыв', organization='фысчя', work_number='89991575959', own_number='89991212222')
    # print(c)
