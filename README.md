![foodgram_workflow](https://github.com/john-neg/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Foodgram

Продуктовый помощник _(Practicum by Yandex education project)_

Проект доступен по адресу - http://62.84.112.55/
Панель администратора:
Логин / пароль: admin

Документация API - http://62.84.112.55/api/docs/

## Технологии:

Foodgram учебный проект базирующийся на:
- Python 3.10
- Django 3.2.16
- Docker 20.10.18
- Nginx 1.22.0
- PostgreSQL 13.0

## Описание:

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Зарегистрированные пользователи могут публиковать рецепты, добавлять рецепты в список желаемого и покупок. Для рецептов из списка покупок можно скачать список ингредиентов.

Незарегистрированные пользователи могут просматривать рецепты.

---

## Установка и запуск с помощью Docker

### Установить переменные окружения

```sh
nano infra/.env
```

#### Содержимое файла .env

```
SECRET_KEY='key'
DEBUG=False
ALLOWED_HOSTS='localhost web 127.0.0.1'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres-pass
DB_HOST=db
DB_PORT=5432
```

### Запуск docker-compose

```sh
cd infra
docker compose up -d --build
```

### Применения миграций

```sh
docker compose exec web python manage.py migrate
```

### Загрузка данных в БД

```sh
docker compose exec web python manage.py loaddata data/dump.json

```

### Создание суперпользователя

```sh
docker compose exec web python manage.py createsuperuser --username=admin --email=admin@admin.ru
```

### Сбор статики в /static/

```sh
docker compose exec web python manage.py collectstatic --no-input
```
### Копирование картинок в /media/

```sh
docker compose exec web cp -r data/images/ media/
```

## Author info:
Evgeny Semenov

## License
MIT