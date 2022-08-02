from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.models.services import (
    Service,
    ServiceRequirement,
    FAQ,
)

from api.serializers.services import (

    ServiceSerializer,
    ServiceRequirementSerializer,
    FAQSerializer,
)


class ServiceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceRequirementViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceRequirementSerializer

    def get_queryset(self):
        return ServiceRequirement.objects.filter(service_id=self.kwargs['service_pk'])

    def get_serializer_class(self):
        return {'service_id': self.kwargs['pk']}


class FAQViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FAQSerializer

    def get_queryset(self):
        return FAQ.objects.filter(service_id=self.kwargs['service_pk'])

    def get_serializer_context(self):
        return {'service_id': self.kwargs['service_pk']}
