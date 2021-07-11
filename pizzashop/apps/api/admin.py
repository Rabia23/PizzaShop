"""Api admin file."""
from django.contrib import admin

from apps.api.models import Menu, Order, OrderLine


class MenuAdmin(admin.ModelAdmin):
    """Menu model admin.

    Parameters
    ----------
    admin : django.contrib
    """

    list_display = ("id", "name", "price")


admin.site.register(Menu, MenuAdmin)


class OrderAdmin(admin.ModelAdmin):
    """Order model admin.

    Parameters
    ----------
    admin : django.contrib
    """

    list_display = ("id", "user", "amount", "created_at", "updated_at")


admin.site.register(Order, OrderAdmin)


class OrderLineAdmin(admin.ModelAdmin):
    """Order line model admin.

    Parameters
    ----------
    admin : django.contrib
    """

    list_display = ("id", "order", "menu", "quantity")


admin.site.register(OrderLine, OrderLineAdmin)
