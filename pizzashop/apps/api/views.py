"""Api views file."""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.api.models import Order, OrderLine
from apps.api.serializers import OrderLineSerializer, OrderSerializer
from apps.pagination import StandardResultsSetPagination


@swagger_auto_schema(
    request_body=OrderSerializer,
    responses={
        201: "Created",
        400: "Bad Request",
        200: "OK",
        204: "No Content",
    },
)
class OrderViewSet(viewsets.ModelViewSet):
    """Order viewset.

    It automatically provides `list`, `create`, `retrieve`
    and `destroy` actions.

    Parameters
    ----------
    viewsets : rest_framework
    """

    queryset = Order.objects.all().order_by("-id")
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination


@swagger_auto_schema(
    request_body=OrderLineSerializer,
    responses={200: "Updated", 400: "Bad Request"},
)
class OrderLineViewSet(viewsets.ModelViewSet):
    """Order line viewset.

    It automatically provides `patch` action.

    Parameters
    ----------
    viewsets : rest_framework
    """

    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer
    permission_classes = (IsAuthenticated,)
