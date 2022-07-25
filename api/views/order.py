from rest_framework import status

from api.models.order import Order, Cart, Service, ServiceDescription, ServiceRequirement, FAQ, TextField, ImageField, \
    Field
from api.serializers.order import OrderSerializer, CartSerializer, ServiceSerializer, ServiceDescriptionSerializer, \
    ServiceRequirementSerializer, FAQSerializer, TextFieldSerializer, ImageFieldSerializer, FileFieldSerializer
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


    def get_serializer_context(self):
        # print(self.request.data['service'])
        (cart, created) = Cart.objects.get_or_create(customer_id=self.request.user.id)
        return {'cart_id': cart.id}

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

    def create(self, request, *args, **kwargs):

        if isinstance(request.data, list):
            for requirement in self.request.data:
                if requirement['type'] == 'textField':
                    context = {
                        'service_id': self.kwargs['service_pk'],
                        'text': ''
                    }
                if requirement['type'] == 'imageField':
                    context = {
                        'service_id': self.kwargs['service_pk'],
                        'upload_image': ''
                    }
                if requirement['type'] == 'fileField':
                    context = {
                        'service_id': self.kwargs['service_pk'],
                        'upload_file': ''
                    }
                serializer = self.get_serializer(data=requirement, context=context, many=False)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
        else:
            if self.request.data['type'] == 'textField':
             context = {
                    'service_id': self.kwargs['service_pk'],
                    'text': ''
                }
            if self.request.data['type'] == 'imageField':
             context = {
                    'service_id': self.kwargs['service_pk'],
                    'upload_image': ''
                }
            if self.request.data['type'] == 'fileField':
                context = {
                    'service_id': self.kwargs['service_pk'],
                    'upload_file': ''
                }
            serializer = self.get_serializer(data=request.data, context=context, many=False)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            service_requirement = ServiceRequirement.objects.get(id=self.kwargs['pk'])
            if service_requirement.type == 'textField':
                return TextFieldSerializer
            if service_requirement.type == 'imageField':
                return ImageFieldSerializer
            if service_requirement.type == 'fileField':
                return FileFieldSerializer
        return ServiceRequirementSerializer

    def get_queryset(self):
        return ServiceRequirement.objects.filter(service_id=self.kwargs['service_pk'])

    def get_serializer_context(self):
        if self.request.method == 'PUT':
            return {'service_requirement_id': self.kwargs['pk']}
        context = super(ServiceRequirementViewSet, self).get_serializer_context()
        return context



class FAQViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_queryset(self):
        return FAQ.objects.filter(service_id=self.kwargs['service_pk'])

    def get_serializer_context(self):
        return {'service_id': self.kwargs['service_pk']}

#
# class RequirementFieldViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]
#
#     # (service_requirement, created) = ServiceRequirement.objects.get_or_create(customer_id=self.request.user.id)
#
#     def get_queryset(self):
#
#         # if self.request.method == 'POST':
#         #     if self.request.data['type'] == 'text':
#         #         return TextField.objects.filter(service_id=self.kwargs['service_pk'])
#         #
#         #     if self.request.data['type'] == 'image':
#         #         return ImageField.objects.filter(service_id=self.kwargs['service_pk'])
#
#         return ServiceRequirement.objects.filter(service_id=self.kwargs['service_pk'])
#
#     # def get_serializer(self, *args, **kwargs):
#     #     serializer_class = self.get_serializer_class()
#     #     kwargs['context'] = self.get_serializer_context()
#     #     return serializer_class(*args, **kwargs)
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             if self.request.data['type'] == 'text':
#                 return TextFieldSerializer
#             return ImageFieldSerializer
#         return ServiceRequirementSerializer
#
#     def get_serializer_context(self):
#         (service_requirement, created) = ServiceRequirement.objects.get_or_create(service_id=self.kwargs['service_pk'])
#         service_requirement.title = self.request.data['title']
#         service_requirement.details = self.request.data['details']
#         service_requirement.hint = self.request.data['hint']
#         service_requirement.type = self.request.data['type']
#         service_requirement.save()
#
#         return {'service_requirement_id': service_requirement.id, 'service_id': self.kwargs['service_pk']}
