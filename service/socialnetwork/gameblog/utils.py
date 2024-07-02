from django.utils.translation import gettext as _

menu = [
    {"title": _("Моя лента"), "url_name": "posts:list-posts"},
    {"title": _("Игровые события"), "url_name": "#"},
    {"title": _("Команды"), "url_name": "teams:index"},
    {"title": _("Магазин 🛒"), "url_name": "shop:products-list"},
    {"title": _("Настройки ⚙"), "url_name": "#"},
]

sidebar = [
    {"url_name": "gameblog:main", "icon": "bx bx-grid-alt", "tooltip": _("Главная")},
    {"url_name": "#", "icon": "bx bx-bell", "tooltip": _("Уведомления")},
    {
        "url_name": "chats:list",
        "icon": "bx bx-message-square-detail",
        "tooltip": _("Чат"),
    },
    {"url_name": "#", "icon": "bx bx-info-circle", "tooltip": _("Поддержка")},
    {
        "url_name": "users:profile_middleware",
        "icon": "bx bx-user",
        "tooltip": _("Профиль"),
    },
]
