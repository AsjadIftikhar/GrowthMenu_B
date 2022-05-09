from api.models.order import Order
from api.serializers.order import OrderSerializer
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from profiles.models import Customer


class OrderViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def order_list(self, request):
        (customer, created) = Customer.objects.get_or_create(
                    user_id=request.user.id)
        queryset = Order.objects.filter(customer=customer)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

