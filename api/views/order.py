from api.models.order import Order, Cart, Service, ServiceDescription, ServiceRequirement
from api.serializers.order import OrderSerializer, CartSerializer, ServiceSerializer, ServiceDescriptionSerializer, \
    ServiceRequirementSerializer
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from profiles.models import Customer


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]

    @action(detail=False, methods=['GET', 'POST', 'PUT'], permission_classes=[IsAuthenticated])
    def order_list(self, request):
        (cart, created) = Cart.objects.get_or_create(
            customer_id=request.user.id)
        queryset = Order.objects.filter(cart=cart)
        if request.method == 'GET':
            serializer = OrderSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = OrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


# class OrderViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     filter_backends = [DjangoFilterBackend]
#
#     @action(detail=False, methods=['GET', 'POST', 'PUT'], permission_classes=[IsAuthenticated])
#     def order_list(self, request):
#         (customer, created) = Customer.objects.get_or_create(
#             user_id=request.user.id)
#         queryset = Order.objects.filter(customer=customer)
#         if request.method == 'GET':
#             serializer = OrderSerializer(queryset, many=True)
#             return Response(serializer.data)
#         elif request.method == 'POST':
#             serializer = OrderSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)


# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminUser]
#
#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)

class CartViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user

        (customer_id, created) = Customer.objects.only('id').get_or_create(
            user_id=user.id)

        return Order.objects.filter(customer_id=customer_id)


class ServiceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceDescriptionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ServiceDescription.objects.all()
    serializer_class = ServiceDescriptionSerializer


class ServiceRequirementViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ServiceRequirement.objects.all()
    serializer_class = ServiceRequirementSerializer
