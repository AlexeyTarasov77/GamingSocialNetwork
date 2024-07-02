# Игровая социальная сеть

![Python Version](https://img.shields.io/badge/python-3.12-blue)
![Django Version](https://img.shields.io/badge/django-5.0-green)
![DjangoRestFramework](https://img.shields.io/badge/DjangoRestFramework-3.12-green)
![Redis](https://img.shields.io/badge/Redis-6.0-red)
![Celery](https://img.shields.io/badge/Celery-5.1.2-cyan)
![Ajax](https://img.shields.io/badge/Ajax-technology-orange)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow)
![HTMX](https://img.shields.io/badge/HTMX-2.0-blue)
![Docker](https://img.shields.io/badge/Docker-20.10.7-blue)
![TailWind CSS](https://img.shields.io/badge/TailWind_CSS-2.2.19-blue)
![Postgresql](https://img.shields.io/badge/Postgresql-15.0-blue)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-orange)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Open Source](https://img.shields.io/badge/Open%20Source-❤️-blue)
![Made by](https://img.shields.io/badge/Made%20by-AlexeyTarasov77-brightgreen)

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
- **chats**: Чаты пользователей (в разработке).
- **coupons**: Купоны для покупок в магазине.
- **events**: Игровые события (запланировано в будущем).
- **gameblog**: Главное приложение, содержит главную страницу и функционал, переиспользуемый другими приложениями.
- **gameteams**: Игровые команды.
- **orders**: Заказы (покупка продуктов в приложении).
- **payment**: Взаимодействие с платежной системой.
- **posts**: Публикации (посты, новости, статьи).
- **users**: Профиль пользователя, авторизация, регистрация, 
    взаимодействия пользователей (подписки, друзья ...).
- **core**: Не является как таковым приложением, содержит сущности переиспользуемые другими приложениями

#### Дерево структуры 
```bash
├── Dockerfile
├── docker-compose.yml
├── package-lock.json
├── package.json
├── requirements.txt
└── socialnetwork
    ├── actions
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── templates
    │   │   └── actions
    │   │       └── ...
    │   └── utils.py
    ├── api
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── posts_api
    │   │   ├── __init__.py
    │   │   ├── serializers.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   ├── search_api
    │   │   ├── __init__.py
    │   │   ├── client.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   ├── urls.py
    │   └── users_api
    │       ├── __init__.py
    │       ├── serializers.py
    │       ├── urls.py
    │       └── views.py
    ├── cart
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── cart.py
    │   ├── context_processors.py
    │   ├── models.py
    │   ├── templates
    │   │   └── cart
    │   │       └── ...
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── factories.py
    │   │   └── test_views.py
    │   ├── urls.py
    │   └── views.py
    ├── chats
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── consumers.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── routing.py
    │   ├── services
    │   │   ├── __init__.py
    │   │   └── chats_service.py
    │   ├── static
    │   │   └── chats
    │   │       └── ...
    │   ├── templates
    │   │   └── chats
    │   │       └── ...
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── factories.py
    │   │   └── test_views.py
    │   ├── urls.py
    │   └── views.py
    ├── core
    │   ├── handle_cache.py
    │   ├── mixins.py
    │   ├── models.py
    │   ├── redis_connection.py
    │   ├── utils.py
    │   └── views.py
    ├── coupons
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── factories.py
    │   │   └── test_views.py
    │   ├── urls.py
    │   └── views.py
    ├── events
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── gameblog
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── consumers.py
    │   ├── context_processors.py
    │   ├── mixins.py
    │   ├── models.py
    │   ├── routing.py
    │   ├── static
    │   │   └── gameblog
    │   │       └── ...
    │   ├── templates
    │   │   └── gameblog
    │   │       └── ...
    │   ├── templatetags
    │   │   ├── __init__.py
    │   │   └── gameblog_tags.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── utils.py
    │   └── views.py
    ├── gameshop
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── index.py
    │   ├── models.py
    │   ├── recommender.py
    │   ├── static
    │   │   └── gameshop
    │   │       └── ...
    │   ├── templates
    │   │   └── gameshop
    │   │       └── ...
    │   ├── templatetags
    │   │   ├── __init__.py
    │   │   └── shop_tags.py
    │   ├── tests
    │   │   ├── factories.py
    │   │   └── test_views.py
    │   ├── urls.py
    │   └── views.py
    ├── gameteams
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── services
    │   │   ├── __init__.py
    │   │   ├── ad_service.py
    │   │   └── team_service.py
    │   ├── signals.py
    │   ├── static
    │   │   └── gameteams
    │   │       └── ...
    │   ├── templates
    │   │   └── gameteams
    │   │       └── ...
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── factories.py
    │   │   └── test_views.py
    │   ├── urls.py
    │   └── views.py
    ├── general_log.log
    ├── locale
    │   ├── en
    │   │   └── LC_MESSAGES
    │   │       ├── django.mo
    │   │       └── django.po
    │   ├── ru
    │   │   └── LC_MESSAGES
    │   │       ├── django.mo
    │   │       └── django.po
    │   └── ukr
    │       └── LC_MESSAGES
    │           ├── django.mo
    │           └── django.po
    ├── manage.py
    ├── orders
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── tasks.py
    │   ├── templates
    │   │   └── orders
    │   │       └── ...
    │   ├── templatetags
    │   │   ├── __init__.py
    │   │   └── orders_tags.py
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── factories.py
    │   │   └── test_views.py
    │   ├── urls.py
    │   └── views.py
    ├── payment
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── static
    │   │   └── payment
    │   │       └── ...
    │   ├── tasks.py
    │   ├── templates
    │   │   └── payment
    │   │       └── ...
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py
    │   └── webhooks.py
    ├── posts
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── index.py
    │   ├── mixins.py
    │   ├── models.py
    │   ├── services
    │   │   ├── __init__.py
    │   │   ├── constants.py
    │   │   ├── m2m_toggle.py
    │   │   └── posts_service.py
    │   ├── static
    │   │   └── posts ...    
    │   ├── tasks.py
    │   ├── templates
    │   │   └── posts
    │   │       ├── ...
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── factories.py
    │   │   └── test_views.py
    │   ├── urls.py
    │   ├── utils.py
    │   └── views.py
    ├── socialnetwork
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── celery.py
    │   ├── routing.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── static
    │   ├── base.css
    │   ├── base.js
    │   ├── notifications.js
    │   ├── search.js
    │   └── tw
    │       ├── tailwind-input.css
    │       └── tailwind-output.css
    ├── tailwind.config.js
    ├── templates
    │   ├── base.html
    │   ├── includes
    │   │   └── pagination.html
    │   └── notifications.html
    └── users
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── decorators.py
        ├── forms.py
        ├── models.py
        ├── serializers.py
        ├── services
        │   ├── __init__.py
        │   └── users_service.py
        ├── signals.py
        ├── static
        │   └── users
        │       ├── ...
        ├── templates
        │   └── users
        │       ├── ...
        ├── tests
        │   ├── __init__.py
        │   └── factories.py
        ├── urls.py
        └── views.py
```

### Стек технологий

- Python 3.12
- Django 5.0
- DjangoRestFramework
- Redis
- Celery
- Ajax
- JavaScript
- HTMX
- Docker
- TailWind CSS
- Postgresql

## Установка

### Шаги установки

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/AlexeyTarasov77/GamingSocialNetwork.git
    cd service
    ```
2. Создайте .env файл в корне django проекта (BASE_DIR) и заполните его соответствующими данными. (Образец файла можно найти в service/socialnetwork/.env.example):

    ```bash
    cp .env.example .env
    ```
3. Сборка проекта (Может занять несколько минут):

    ```bash
    docker compose build
    ```

4. Запуск проекта:

    ```bash
    docker compose up
    ```

## Использование

### Запуск сервера разработки

После установки если проект уже собран, запустите через:

```bash
docker compose up
```

# Основные возможности

## Команды пользователей

Пользователи могут создавать и присоединяться к командам для совместного взаимодействия и участия в различных мероприятиях. Команды могут иметь свои собственные страницы с новостями, событиями и обсуждениями.

![Команды пользователей](readme_images/teams.png)

## Обмен контентом

Пользователи могут обмениваться различным контентом, таким как посты, статьи и новости. Эта функциональность позволяет делиться важной информацией, обсуждать новости и писать статьи на интересующие темы.

![Просмотр постов](readme_images/posts-create.png)
![Создание постов](readme_images/posts-create.png)

## Чаты между пользователями

Для удобного общения предусмотрены чаты между пользователями. Это могут быть как приватные переписки, так и групповые чаты, где можно обсуждать различные темы и обмениваться сообщениями в реальном времени.

![Все чаты](readme_images/chat-create.png)
![Переписка в чате](readme_images/chatroom.png)

## Онлайн магазин игр

В нашем проекте есть онлайн-магазин, где пользователи могут покупать игры. Магазин предлагает широкий ассортимент игр, скидки и специальные предложения.

![Онлайн магазин игр](readme_images/shop-products.png)
![Корзина](readme_images/shop-cart.png)

## Взаимодействия между пользователями

Пользователи могут взаимодействовать друг с другом различными способами:
- **Подписки**: Подписывайтесь на интересных пользователей, чтобы получать обновления их контента.
- **Подписчики**: Следите за тем, кто подписан на вас.
- **Друзья**: Добавляйте друзей для более тесного общения и взаимодействия.

![Профиль пользователя](readme_images/profile.png)

## Внесение вклада

Мы рады, что вы хотите внести свой вклад в наш проект! Пожалуйста, следуйте этим шагам, чтобы помочь улучшить Gaming Social Network:

1. **Форк репозитория**: Нажмите на кнопку "Fork" в правом верхнем углу этой страницы, чтобы создать копию репозитория в вашем аккаунте GitHub.

2. **Клонируйте форкнутый репозиторий** на ваш локальный компьютер:
    ```sh
    git clone https://github.com/AlexeyTarasov77/GamingSocialNetwork.git
    cd GamingSocialNetwork
    ```

3. **Создайте новую ветку** для ваших изменений:
    ```sh
    git checkout -b имя-вашей-ветки
    ```

4. **Внесите изменения** в коде или документации. Убедитесь, что вы протестировали свои изменения перед коммитом.

5. **Коммит ваших изменений**:
    ```sh
    git add .
    git commit -m "Описание ваших изменений"
    ```

6. **Отправьте изменения** в ваш форкнутый репозиторий:
    ```sh
    git push origin имя-вашей-ветки
    ```

7. **Создайте Pull Request**: Перейдите в оригинальный репозиторий и нажмите на кнопку "New Pull Request". Опишите ваши изменения и отправьте запрос на слияние.

Спасибо за ваш вклад! Ваши изменения помогут сделать наш проект лучше.


## Прогон тестов

1. Запустите проект пользуясь инструкциями в секции [Использование](#использование).

2. Войдите в оболочку терминала внутри контейнера с приложением.

```bash
docker exec -it sc-service sh
```

3. Для запуска тестов выполните команду:

```bash
python3 manage.py test
```
