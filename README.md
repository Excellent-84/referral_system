## Реферальная система.

### Описание проекта:

 - Авторизация по номеру телефона. Первый запрос на ввод номера телефона. Имитация отправки 4-х значного кода авторизации (задержка на сервере 2 сек). Второй запрос на ввод кода
 - Если пользователь ранее не авторизовывался, то записывается в бд
 - Запрос на профиль пользователя
 - Пользователю при первой авторизации присваваетя рандомно сгенерированный 6-значный инвайт-код (цифры и символы)
 - В профиле у пользователя есть возможность ввести чужой инвайт-код (при вводе проверяется на существование). В своем профиле можно активировать только 1 инвайт код, если пользователь уже когда-
то активировал инвайт-код, то он выводится его в профиле пользователя
 - В API профиля выводится список пользователей (номеров телефона), которые ввели инвайт код текущего пользователя.
 - Так же в проекте реализована аутентификация по JWT-токену, минималистичный интерфейс на Django Templates, документация ReDoc


### Стек технологий:
<img src="https://img.shields.io/badge/Python-FFFFFF?style=for-the-badge&logo=python&logoColor=3776AB"/><img src="https://img.shields.io/badge/django-FFFFFF?style=for-the-badge&logo=django&logoColor=082E08"/><img src="https://img.shields.io/badge/Django REST Framework-FFFFFF?style=for-the-badge&logo=&logoColor=361508"/><img src="https://img.shields.io/badge/PostgreSQL-FFFFFF?style=for-the-badge&logo=PostgreSQL&logoColor=4169E1"/>

### Как запустить проект:

##### Клонировать репозиторий и перейти в проект:
```bash
$ git clone https://github.com/Excellent-84/referral_system.git
$ cd referral_system/
```

##### Cоздать и активировать виртуальное окружение:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

##### Установить зависимости из файла requirements.txt:

```bash
$ pip install -r requirements.txt
```

##### Создать файл .env и указать необходимые токены по примеру .env.example:
```bash
$ touch .env
```

##### Выполнить миграции:

```bash
$ cd referral
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

##### Создать суперпользователя:

```bash
$ python3 manage.py createsuperuser
```

##### Запустить проект:

```bash
$ python3 manage.py runserver
```

### Примеры запросов к API:

##### Авторизация пользователя:
POST запрос http://{ip-адрес}/api/auth/
```bash
{
    "phone_number": "+79000000000"
}
```
##### Ответ:
```bash
{
    "message": "Код активации: 4293"
}
```

##### Верификация и получение Токена:
POST запрос http://{ip-адрес}/api/verify/
```bash
{
    "code": "4293"
}
```
##### Ответ:
```bash
{
    "Токен": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX..."
}
```

##### Получение профиля пользователя (необходимо передать Токен):
GET запрос http://{ip-адрес}/api/profile/

##### Ответ:
```bash
{
    "phone_number": "+79000000000",
    "invite_code": "ZRRUML",
    "activated_invite_code": "8Q2YX0",
    "referrals_count": 0,
    "referrals": []
}
```

##### Активация инвайт-кода:
POST запрос http://{ip-адрес}/api/activate-invite/
```bash
{
    "invite_code": "8Q2YX0"
}
```
##### Ответ:
```bash
{
    "message": "Инвайт-код активирован"
}
```

##### Получение всех пользователей:
GET запрос http://{ip-адрес}/api/users/

##### Ответ:
```bash
[
    {
        "phone_number": "+78563214522",
        "invite_code": "0DQ68S",
        "activated_invites_count": 1
    },
    {
        "phone_number": "+79000000000",
        "invite_code": "MP3FFX",
        "activated_invites_count": 5
    }
    ...
]
```

##### Подробную версию запросов можно посмотреть в документации ReDoc:
http://{ip-адрес}/redoc/

#### Автор: [Горин Евгений](https://github.com/Excellent-84)
