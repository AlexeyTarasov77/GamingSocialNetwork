from .utils import menu, sidebar

def menu_links(request):
    return {'headermenu':menu}

def sidebar_links(request):
    return {
        'sidebar_links_default': sidebar,
        'sidebar_links_optional': getattr(request, 'sidebar_links', None)
    }