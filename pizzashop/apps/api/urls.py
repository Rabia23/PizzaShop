"""Api urls file."""
from django.urls import path

from apps.api.views import OrderLineViewSet, OrderViewSet

order_list = OrderViewSet.as_view({"get": "list", "post": "create"})
order_detail = OrderViewSet.as_view({"get": "retrieve", "delete": "destroy"})
order_line_detail = OrderLineViewSet.as_view({"patch": "partial_update"})

urlpatterns = [
    path("orders/", order_list, name="order-list"),
    path("orders/<int:pk>/", order_detail, name="order-detail"),
    path("order-lines/<int:pk>/", order_line_detail, name="order-line-detail"),
]
