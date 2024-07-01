from api.search_api.client import get_list_indices

from .utils import menu, sidebar


def menu_links(request):
    return {"headermenu": menu}


def sidebar_links(request):
    return {
        "sidebar_links_default": sidebar,
    }


def indices(request):
    return {"indices": get_list_indices()}
