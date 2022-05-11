from api.models.order import Order
from api.serializers.order import OrderSerializer
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
        (customer, created) = Customer.objects.get_or_create(
                    user_id=request.user.id)
        queryset = Order.objects.filter(customer=customer)
        if request.method == 'GET':
            serializer = OrderSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = OrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # def order_list2(self, request):
        #     (customer, created) = Customer.objects.get_or_create(
        #         user_id=request.user.id)
        #     queryset = Order.objects.filter(customer=customer)
        #     if request.method == 'GET':
        #         serializer = OrderSerializer(queryset, many=True)
        #         return Response(serializer.data)
        #     elif request.method == 'POST':
        #         serializer = OrderSerializer(data=request.data)
        #         serializer.is_valid(raise_exception=True)
        #         serializer.save()
        #         return Response(serializer.data)



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