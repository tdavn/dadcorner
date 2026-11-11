from decimal import Decimal
from django.conf import settings
from kitchen.models import Dish


class Menu:
    def __init__(self, request):
        """
        Initialize the menu.
        """
        self.session = request.session
        menu = self.session.get(settings.MENU_SESSION_ID)
        if not menu:
            # save an empty menu in the session
            menu = self.session[settings.MENU_SESSION_ID] = {}
        self.menu = menu

    def add(self, dish, quantity=1, override_quantity=False):
        """
        Add a dish to the menu or update its quantity.
        """
        dish_id = str(dish.id)
        if dish_id not in self.menu:
            self.menu[dish_id] = {'quantity': 0, 'calories': str(dish.calories)}
        if override_quantity:
            self.menu[dish_id]['quantity'] = quantity
        else:
            self.menu[dish_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, dish):
        """
        Remove a dish from the menu.
        """
        dish_id = str(dish.id)
        if dish_id in self.menu:
            del self.menu[dish_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the menu and get the dishes
        from the database.
        """
        dish_ids = self.menu.keys()
        # get the dish objects and add them to the menu
        dishes = Dish.objects.filter(id__in=dish_ids)
        menu = self.menu.copy()
        for dish in dishes:
            menu[str(dish.id)]['dish'] = dish
        for item in menu.values():
            item['calories'] = Decimal(item['calories'])
            item['total_calories'] = item['calories'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the menu.
        """
        return sum(item['quantity'] for item in self.menu.values())

    def get_total_calories(self):
        return sum(Decimal(item['calories']) * item['quantity'] for item in self.menu.values())

    def clear(self):
        # remove menu from session
        del self.session[settings.MENU_SESSION_ID]
        self.save()