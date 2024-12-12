# Курсовой проект №4

<i>Это Django-проект менеджера почтовых рассылок MailingManager</i>

## Описание проекта

## Установка:

1. Клонируйте репозиторий:

```
https://github.com/AlexandrPavlushenko/MailingManager.git
```

2. Установите зависимости:

```
pip install -r requirements.txt
```

3. Создайте и заполните данными файл <b>.env</b> по шаблону <b>.env.sample</b>, который находится в корне проекта

4. Создайте и примините миграции
```
python manage.py makemigrations
python manage.py migrate
```

5.В проекте есть фикстура для создания группы пользователей - менеджер

```
   python manage.py loaddata users_groups.json --format json
```
## Использование:

В терминале введите команду запуска сервера: <b><i>python manage.py runserver</i></b>
В проекте есть возможность запуска рассылки из командной строки:
```
python manage.py send_mailing <mailing_id>
```
где <mailing_id> - номер созданной рассылки

Так же есть кастомная команда создания суперпользователя
```
python manage.py csu

```
