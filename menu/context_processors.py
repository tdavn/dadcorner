from .menu import Menu


def menu(request):
    return {'menu': Menu(request)}