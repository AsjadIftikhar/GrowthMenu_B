from api.models.order import Order, Cart, Service, ServiceDescription, ServiceRequirement, FAQ, TextField, ImageField, Field
from api.serializers.order import OrderSerializer, CartSerializer, ServiceSerializer, ServiceDescriptionSerializer, \
    ServiceRequirementSerializer, FAQSerializer, TextFieldSerializer, ImageFieldSerializer, FieldSerializer
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

    # def get_queryset(self):
    #     return Order.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_context(self):
        # print(self.request.data['service'])
        (cart, created) = Cart.objects.get_or_create(customer_id=self.request.user.id)
        return {'cart_id': cart.id}
    # filter_backends = [DjangoFilterBackend]
    #
    # @action(detail=False, methods=['GET', 'POST', 'PUT'], permission_classes=[IsAuthenticated])
    # def order_list(self, request):
    #     (cart, created) = Cart.objects.get_or_create(
    #         customer_id=request.user.id)
    #     queryset = Order.objects.filter(cart=cart)
    #     if request.method == 'GET':
    #         serializer = OrderSerializer(queryset, many=True)
    #         return Response(serializer.data)
    #     elif request.method == 'POST':
    #         serializer = OrderSerializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)


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
    # queryset = ServiceDescription.objects.all()
    serializer_class = ServiceDescriptionSerializer

    def get_queryset(self):
        return ServiceDescription.objects.filter(service_id=self.kwargs['service_pk'])

    def get_serializer_context(self):
        return {'service_id': self.kwargs['service_pk']}

    # def get_serializer_class(self):
    #     if self.request.data



class ServiceRequirementViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # queryset = ServiceRequirement.objects.all()
    serializer_class = ServiceRequirementSerializer

    def get_queryset(self):
        # print(self.kwargs)
        return ServiceRequirement.objects.filter(service_id=self.kwargs['service_pk'])

    def get_serializer_context(self):
        # print(self.kwargs)
        return {'service_id': self.kwargs['service_pk']}


class FAQViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_queryset(self):
        return FAQ.objects.filter(service_description_id=self.kwargs['service_description_pk'])

    def get_serializer_context(self):
        return {'service_description_id': self.kwargs['service_description_pk']}

class RequirementFieldViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    # (service_requirement, created) = ServiceRequirement.objects.get_or_create(customer_id=self.request.user.id)

    def get_queryset(self):

        # if self.request.method == 'POST':
        #     if self.request.data['type'] == 'text':
        #         return TextField.objects.filter(service_id=self.kwargs['service_pk'])
        #
        #     if self.request.data['type'] == 'image':
        #         return ImageField.objects.filter(service_id=self.kwargs['service_pk'])

        return ServiceRequirement.objects.filter(service_id=self.kwargs['service_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            if self.request.data['type'] == 'text':
                return TextFieldSerializer
            return ImageFieldSerializer
        return ServiceRequirementSerializer

    def get_serializer_context(self):
        (service_requirement, created) = ServiceRequirement.objects.get_or_create(service_id=self.kwargs['service_pk'])
        service_requirement.title = self.request.data['title']
        service_requirement.details = self.request.data['details']
        service_requirement.hint = self.request.data['hint']
        service_requirement.type = self.request.data['type']
        service_requirement.save()

        return {'service_requirement_id':service_requirement.id,'service_id': self.kwargs['service_pk']}