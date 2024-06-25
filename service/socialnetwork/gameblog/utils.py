from django.utils.translation import gettext as _

# links to display in header
menu = [
    {"title": _("Моя лента"), "url_name": "posts:list-posts", "id": "menu-item-1"},
    {"title": _("Игровые события"), "url_name": "#", "id": "menu-item-3"},
    {"title": _("Команды"), "url_name": "teams:index", "id": "menu-item-4"},
    {"title": _("Магазин 🛒"), "url_name": "shop:products-list", "id": "menu-item-5"},
    {"title": _("Настройки ⚙"), "url_name": "#", "id": "menu-item-6"},
]

# links to display in sidebar
sidebar = [
    {"url_name": "gameblog:main", "icon": "bx bx-grid-alt", "tooltip": _("Главная")},
    {"url_name": "#", "icon": "bx bx-bell", "tooltip": "Уведомления"},
    {"url_name": "#", "icon": "bx bx-message-square-detail", "tooltip": _("Cooбщения")},
    {"url_name": "#", "icon": "bx bx-info-circle", "tooltip": _("Поддержка")},
    {
        "url_name": "users:profile_middleware",
        "icon": "bx bx-user",
        "tooltip": _("Профиль"),
    },
]
