"""Api serializers file."""
import logging

from django.contrib.auth.models import User
from django.db import transaction

from rest_framework import serializers

from apps.api.models import Menu, Order, OrderLine


logger = logging.getLogger(__name__)

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class MenuSerializer(serializers.ModelSerializer):
    """Menu serializer class.

    Parameters
    ----------
    serializers : rest_framework
    """

    class Meta:  # noqa: D106
        model = Menu
        # display all the model fields except `id`
        exclude = ["id"]


class OrderLineSerializer(serializers.ModelSerializer):
    """Order line serializer class.

    Parameters
    ----------
    serializers : rest_framework
    """

    menu = MenuSerializer()

    class Meta:  # noqa: D106
        model = OrderLine
        # display all the model fields except `id`
        exclude = ["id"]

    def update(self, instance, validated_data) -> OrderLine:
        """Update the order line instance.

        Parameters
        ----------
        instance : apps.api.models.OrderLine
        validated_data : dict

        Returns
        -------
        apps.api.models.OrderLine
            returns updated order line instance
        """
        instance = super(OrderLineSerializer, self).update(
            instance, validated_data
        )
        instance.order.amount += instance.menu.price * instance.quantity
        instance.order.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer class.

    Parameters
    ----------
    serializers : rest_framework
    """

    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    order_lines = OrderLineSerializer(many=True, required=False)
    created_at = serializers.DateTimeField(
        format=DATETIME_FORMAT, read_only=True
    )
    updated_at = serializers.DateTimeField(
        format=DATETIME_FORMAT, read_only=True
    )

    class Meta:  # noqa: D106
        model = Order
        # display all the model fields except `id`
        exclude = ["id"]

    def validate(self, data: dict) -> dict:
        """
        Validate the serializer data.

        Parameters
        ----------
        data : dict

        Returns
        -------
        dict
            returns validated data if no error occurs

        Raises
        ------
        serializers.ValidationError
            check for the following cases:
            - If required param is missing.
            - If invalid param is given.
            - If user doesn't exist.
            - If menu doesn't exist.
        """
        valid_required_params = ("user", "lines")
        # validates input params
        if any(
            map(
                lambda x: x not in self.initial_data.keys(),
                valid_required_params,
            )
        ):
            raise serializers.ValidationError(
                f"Params missing. Required params are {valid_required_params}"
            )

        if any(
            map(
                lambda x: x not in valid_required_params,
                self.initial_data.keys(),
            )
        ):
            raise serializers.ValidationError(
                f"Not a valid param. Options are {valid_required_params}"
            )

        user = None
        try:
            user = User.objects.get(pk=self.initial_data.get("user"))
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist!")
        else:
            self.initial_data["user"] = user

        for line in self.initial_data.get("lines"):
            menu = None
            try:
                menu = Menu.objects.get(id=line.get("menu"))
            except Menu.DoesNotExist:
                raise serializers.ValidationError(
                    f"Menu id {line.get('menu')} doesn't exist!"
                )
            else:
                line["menu"] = menu

        return self.initial_data

    @transaction.atomic
    def create(self, validated_data) -> Order:
        """
        Create the validated data.

        Parameters
        ----------
        validated_data : dict

        Returns
        -------
        apps.api.models.Order
            returns the created order instance
        """
        lines = validated_data.pop("lines")
        order = None
        try:
            order = Order.objects.create(**validated_data)
        except Exception:
            logger.exception("Unable to create order.")
        else:
            logger.info(f"Order with id {order.id} has been created.")
            amount = 0
            for line in lines:
                menu = line.get("menu")
                order_line = None
                try:
                    order_line = OrderLine.objects.create(
                        order=order, menu=menu, quantity=line.get("quantity")
                    )
                except Exception:
                    logger.exception("Unable to create order line.")
                else:
                    logger.info(
                        f"Orderline with id {order_line.id} has been created."
                    )
                    amount += menu.price * order_line.quantity
            order.amount = amount
            order.save()
        return order or {}
