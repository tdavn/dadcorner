from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from kitchen.models import Dish
from .menu import Menu
from .forms import MenuAddDishForm


@require_POST
def menu_add(request, dish_id):
    menu = Menu(request)
    dish = get_object_or_404(Dish, id=dish_id)
    form = MenuAddDishForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        menu.add(dish=dish, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('menu:menu_detail')

@require_POST
def menu_remove(request, dish_id):
    menu = Menu(request)
    dish = get_object_or_404(Dish, id=dish_id)
    menu.remove(dish)
    return redirect('menu:menu_detail')

def menu_detail(request):
    menu = Menu(request)
    for item in menu:
        item['update_quantity_form'] = MenuAddDishForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'menu/detail.html', {'menu': menu})

