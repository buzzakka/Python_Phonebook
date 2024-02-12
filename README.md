# Phonebook

Тестовое задание Effective Mobile. [Ссылка на задание](https://docs.google.com/document/d/1dIH7lY05hNLSluZgOYsRyTrvLmyz4CnNEtJFFXBbS-c/edit) .

Для тестирования запушил базу данных `phonebook.json`, созданную скриптом `fill_bd.py`. Если вы хотите протестировать файл с пустой базой данных, программа создаст
пустой файл `phonebook.json`.

![app gif](/misc/images/app.gif)

## Установка
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