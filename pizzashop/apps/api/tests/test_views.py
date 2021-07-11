"""Views test cases."""
import logging

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.api.models import Menu, Order, OrderLine


class BaseViewSetTestCase(APITestCase):
    """Base viewset test cases.

    Parameters
    ----------
    APITestCase : rest_framework.test
    """

    @classmethod
    def setUpClass(cls):
        """Set up class for viewset test cases."""
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        """Tear down class for viewset test cases."""
        logging.disable(logging.NOTSET)

    def setUp(self):
        """Set up the data for each test case."""
        user = User.objects.create(
            username="rabia", password="rabia", email="rabia@gmail.com"
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        menu_data = [
            {"name": "sicilian pizza", "price": 700},
            {"name": "italian pizza", "price": 500},
        ]
        self.order = Order.objects.create(user=user, amount=1200.00)
        for menu in menu_data:
            menu_obj = Menu.objects.create(**menu)
            OrderLine.objects.create(
                order=self.order, menu=menu_obj, quantity=1
            )


class OrderViewSetTestCase(BaseViewSetTestCase, APITestCase):
    """Order viewset test cases.

    Parameters
    ----------
    BaseViewSetTestCase : rest_framework.test
    APITestCase : rest_framework.test
    """

    def setUp(self):
        """Set up the api url for each test case."""
        super(OrderViewSetTestCase, self).setUp()
        self.url = reverse("order-list")

    def test_url_saves_valid_data_in_db(self):
        """Test that url with valid data saves in the db successfully."""
        data = {
            "user": User.objects.first().id,
            "lines": [{"menu": Menu.objects.first().id, "quantity": 8}],
        }
        res = self.client.post(self.url, data=data, format="json")
        # assert url returns 201 response code
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        json_res = res.json()
        self.assertEqual(json_res["user"], "rabia")
        self.assertEqual(len(json_res["order_lines"]), 1)
        self.assertEqual(json_res["amount"], "5600.00")

    def test_url_with_missing_param_returns_error(self):
        """Test that url returns error if one of the required params is missing."""  # noqa:E501
        data = {"user": User.objects.first().id}
        res = self.client.post(self.url, data=data, format="json").json()

        assert (
            "Params missing. Required params are ('user', 'lines')"
            in res["non_field_errors"]
        )

    def test_url_with_invalid_param_returns_error(self):
        """Test that url returns error if invalid param is given."""
        data = {
            "key": "error",
            "user": User.objects.first().id,
            "lines": [{"menu": Menu.objects.first().id, "quantity": 8}],
        }
        res = self.client.post(self.url, data=data, format="json").json()

        assert (
            "Not a valid param. Options are ('user', 'lines')"
            in res["non_field_errors"]
        )

    def test_url_with_given_order_id_returns_data(self):
        """Test that url with the existing order id in the db returns data."""
        data = Order.objects.values("id").first()
        res = self.client.get(
            reverse("order-detail", kwargs={"pk": data.get("id")})
        ).json()

        # assert that data returns from the api is same as expected_data
        self.assertEqual(res["user"], "rabia")
        self.assertEqual(len(res["order_lines"]), 2)
        self.assertEqual(res["amount"], "1200.00")

    def test_url_with_given_order_id_deletes_data(self):
        """Test that url with the existing order id in the db deletes data."""
        data = Order.objects.values("id").first()
        res = self.client.delete(
            reverse("order-detail", kwargs={"pk": data.get("id")})
        )
        # assert that data is deleted from the db
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class OrderLineViewSetTestCase(BaseViewSetTestCase, APITestCase):
    """Order line viewset test cases.

    Parameters
    ----------
    BaseViewSetTestCase : rest_framework.test
    APITestCase : rest_framework.test
    """

    def test_url_with_given_orderline_id_updates_data(self):
        """Test that url with the existing order line id in the db updates data."""  # noqa:E501
        data = {"quantity": 3}
        line = OrderLine.objects.values("id", "quantity").first()
        # assert the old quantity of the line
        self.assertEqual(line.get("quantity"), 1)
        res = self.client.patch(
            reverse("order-line-detail", kwargs={"pk": line.get("id")}),
            data=data,
            format="json",
        ).json()
        # assert the quantity of the line is updated
        self.assertEqual(res["quantity"], 3)
