# Phonebook

Тестовое задание Effective Mobile. [Ссылка на задание](https://docs.google.com/document/d/1dIH7lY05hNLSluZgOYsRyTrvLmyz4CnNEtJFFXBbS-c/edit) .

![app gif](/misc/images/app.gif)

## Установка
!ВНИМАНИЕ! Для тестирования создан скрипт fill_bd.py . Он генерирует 100 записей с контактами. Для тестирования создайте файл с контактами до запуска приложения, или удалите существующий файл `phonebook.json`.

Установка осуществляется из корневой папки проекта, в которой находится Makefile.

### Установка с запуском приложения
#### Через Makefile
```bash
make all
```
#### Через терминал вручную
```bash
python3 -m venv venv
venv/bin/pip3 install -r requirements.txt
./venv/bin/python3 app.py
```