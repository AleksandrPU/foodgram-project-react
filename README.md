# Описание:

Учебный проект по изучению создания бекэнда для сайта, а также автоматизации разворачивания на сервере сайта с использованием контейнеров.

Сайт предназначен для хранения рецептов блюд с возможностью добавления в избранное и список покупок. Список покупок можно сохранить в csv-файл. Реализована возможность подписки на других пользователей.

# Используемые технологии:

Для создания и управления контейнерами используется [Docker](https://www.docker.com/) с расширением [Compose](https://docs.docker.com/compose/)

Для CI/CD применен [GitHub Actions](https://github.com/features/actions).

## Контейнеры

### Backend

- [Django-3.2](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)

В качестве СУБД используется [PostgreSQL-13](https://www.postgresql.org/).

Для создания токенов и аутентификации пользователей применен [djoser](https://djoser.readthedocs.io/). 

### Frontend

- [NodeJS-13](https://nodejs.org)

### Прокси-сервер

- [NGINX](https://nginx.org)

# Запуск проекта:

## Подготовка к запуску:

1. Для запуска проекта необходимо на сервере установить Docker и расширение Docker-Compose.

1. Создать директорию для проекта. Например, foodgram.

1. Скопировать в эту директорию файл docker-compose.production.yml

1. Создать в этой директории файл с настройками .env по примеру файла .env.example

## Запуск:

1. Скачать подготовленные контейнеры:

```bash
sudo docker compose -f docker-compose.production.yml pull
```

1. Перезапустить контейнеры:

```bash
sudo docker compose -f docker-compose.production.yml down
sudo docker compose -f docker-compose.production.yml up -d
```

1. Выполнить создание базы данных:

```bash
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

1. Выполнить подготовку статики для сайта:

```bash
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```

После запуска сайт доступен по адресу 127.0.0.1:8000 или localhost:8000

## Остановка проекта:

```bash
sudo docker compose -f docker-compose.production.yml down
```

## Обновление:

При необходимости можно обновить запущенные контейнеры повторно выполнив команды из раздела "Запуск".

# Работа с сайтом:

Для использования сайта пользователи должны зарегистрироваться.

## Администрирование:

Создание суперпользователя:

```bash
sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

Управление пользователями возможно в админ зоне сайта 127.0.0.1:8000/admin/

# Примеры запросов к API:

## Регистрация пользователя:

```
POST /api/users/
```

Тело запроса application/json:

```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "password": "string"
}
```

Пример ответа:

HTTP 201 Created
```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "id": 0
}
```

## Получить токен:

```
POST /api/auth/token/login/
```

Тело запроса application/json:

```json
{
  "email": "string",
  "password": "string"
}
```

Пример ответа:

HTTP 200 OK
```json
{
    "auth_token": "string"
}
```

## Получить список пользователей:

```
GET /api/users/
```

Пример ответа:

HTTP 200 OK
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": [
    {
      "email": "string",
      "id": 0,
      "username": "string",
      "first_name": "string",
      "last_name": "string",
      "is_subscribed": false
    }
  ]
}
```

## Получить список рецептов:

```
GET /api/recipes/
```

Пример ответа:

HTTP 200 OK
```
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "string",
          "color": "string",
          "slug": "slug"
        }
      ],
      "author": {
        "email": "string",
        "id": 0,
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "string",
          "measurement_unit": "string",
          "amount": 1
        }
      ],
      "is_favorited": false,
      "is_in_shopping_cart": false,
      "name": "string",
      "image": "string",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

## Полный список эндпоинтов и их параметров

Полный список можно посмотреть по адресу http://127.0.0.1:8000/api/schema/swagger-ui/ или http://127.0.0.1:8000/api/schema/redoc/ при включенной режиме отладки (DJANGO_DEBUG=true в файле настроек .env).

# Автор:

Проект создан Паутовым Александром на основе репозитория [yandex-praktikum/foodgram-project-react](https://github.com/yandex-praktikum/foodgram-project-react)
