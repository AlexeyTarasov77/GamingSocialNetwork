from .utils import menu, sidebar

def menu_links(request):
    return {'headermenu':menu}

def sidebar_links(request):
    return {
        'sidebar_links_default': sidebar,
    }