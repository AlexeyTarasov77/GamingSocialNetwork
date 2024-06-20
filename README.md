# Игровая социальная сеть

Добро пожаловать в проект "Игровая социальная сеть"! Этот проект представляет собой платформу для геймеров, которая включает в себя разнообразные функциональные возможности, такие как корзина покупок, чаты, публикации, игровые команды и многое другое.

## Содержание

- [Описание проекта](#описание-проекта)
- [Структура проекта](#структура-проекта)
- [Установка](#установка)
- [Использование](#использование)

## Описание проекта

Проект "Игровая социальная сеть" предназначен для создания сообщества геймеров, предоставляя различные функции для взаимодействия, обмена контентом и покупок. В проекте предусмотрены такие возможности, как публикации статей и новостей, создание игровых команд, управление корзиной покупок, взаимодействие с платежными системами и многое другое.

## Структура проекта

Проект состоит из следующих приложений:

- **actions**: Сохранение последних действий пользователя на сайте.
- **api**: Частичное API для каждого из приложений (в разработке).
- **cart**: Корзина для покупок.
- **chat**: Чат для пользователей (в разработке).
- **coupons**: Купоны для покупок в магазине.
- **events**: Игровые события (запланировано в будущем).
- **gameblog**: Главное приложение, содержит главную страницу и функционал, переиспользуемый другими приложениями.
- **gameteams**: Игровые команды.
- **orders**: Заказы (покупка продуктов в приложении).
- **payment**: Взаимодействие с платежной системой.
- **posts**: Публикации (посты, новости, статьи).
- **users**: Профиль пользователя, авторизация, регистрация.

### Стек технологий

- Python 3.12
- Django 5.0
- DjangoRestFramework
- Redis
- Celery
- Ajax
- JavaScript
- Docker
- TailWind CSS
- PostgresQL

## Установка

### Шаги установки

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/AlexeyTarasov77/GamingSocialNetwork.git
    cd service
    ```

2. Поднятие проекта

   ```bash
   docker compose up --build
   ```

## Использование

### Запуск сервера разработки

После установки если проект уже собран, запустите через:

```bash
docker compose up