"""Api models file."""
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class Menu(models.Model):
    """Menu model class.

    Parameters
    ----------
    models : django.db
    """

    name = models.CharField(_("name"), max_length=64)
    price = models.DecimalField(_("price"), decimal_places=2, max_digits=12)

    class Meta:  # noqa: D106
        verbose_name = "menu"
        verbose_name_plural = "menus"

    def __str__(self):
        """Str representation of menu model.

        Returns
        -------
        str
            containing item name along with the price of the given object
        """
        return f"{self.name} @ Rs{self.price}"


class Order(models.Model):
    """Order model class.

    Parameters
    ----------
    models : django.db
    """

    user = models.ForeignKey(
        User, related_name="orders", on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        _("amount"), decimal_places=2, max_digits=12, default=0.00
    )
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    class Meta:  # noqa: D106
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self):
        """Str representation of order model.

        Returns
        -------
        str
            containing order id along with the user and amount of the
            given object
        """
        return f"Order no. {self.id} by {self.user} with amount {self.amount}"


class OrderLine(models.Model):
    """Order line model class.

    Parameters
    ----------
    models : django.db
    """

    order = models.ForeignKey(
        Order, related_name="order_lines", on_delete=models.CASCADE
    )
    menu = models.ForeignKey(
        Menu, related_name="order_menus", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(_("quantity"))

    class Meta:  # noqa: D106
        verbose_name = "orderline"
        verbose_name_plural = "orderlines"

    def __str__(self):
        """Str representation of order line model.

        Returns
        -------
        str
            containing order id along with the menu id and quantity of the
            given object
        """
        return f"{self.order_id} has {self.menu_id} X {self.quantity}"
