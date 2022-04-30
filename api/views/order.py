from api.models.order import Order
from api.serializers.order import OrderSerializer
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from profiles.models import Customer


class OrderViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]

    # def get_queryset(self):
    #     queryset = Order.objects.filter(customer__user=self.request.user.id)
    #     print(self.request.user)
    #     return queryset
