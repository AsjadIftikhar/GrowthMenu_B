from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.models.order import (
    Order,
)
from api.serializers.order import (
    OrderSerializer,
    CartSerializer,
)

from profiles.models import Customer


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        # todo Profile Based Permission
        # todo if user is an admin, return all orders
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only('id').get(user_id=user.id)
        Order.objects.filter(customer_id=customer_id)


class CartViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user

        (customer_id, created) = Customer.objects.only('id').get_or_create(
            user_id=user.id)

        return Order.objects.filter(customer_id=customer_id)
