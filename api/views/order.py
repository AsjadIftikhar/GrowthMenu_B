from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.models.order import (
    Order,
    OrderItem,
    Form,
    TextField,
    ImageField,
    FileField,
)
from api.serializers.order import (
    OrderSerializer,
    OrderItemSerializer,
    FormSerializer,
    TextFieldSerializer,
    ImageFieldSerializer,
    FileFieldSerializer,
)

from profiles.models import Customer


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only('id').get(user_id=user.id)
        Order.objects.filter(customer_id=customer_id)


class OrderItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        OrderItem.objects.filter(order_id=self.kwargs['orders_pk'])

    def get_serializer_context(self):
        return {'order_id': self.kwargs['orders_pk']}


class FormViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSerializer

    def get_queryset(self):
        Form.objects.all()


class TextFieldViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TextFieldSerializer

    def get_queryset(self):
        TextField.objects.filter(form_id=self.kwargs['forms_pk'])

    def get_serializer_context(self):
        return {'form_id': self.kwargs['forms_pk']}


class ImageFieldViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageFieldSerializer

    def get_queryset(self):
        ImageField.objects.filter(form_id=self.kwargs['forms_pk'])

    def get_serializer_context(self):
        return {'form_id': self.kwargs['forms_pk']}


class FileFieldViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FileFieldSerializer

    def get_queryset(self):
        FileField.objects.filter(form_id=self.kwargs['forms_pk'])

    def get_serializer_context(self):
        return {'form_id': self.kwargs['forms_pk']}
