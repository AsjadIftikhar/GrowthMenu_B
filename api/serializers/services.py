from rest_framework import serializers

from api.models.order import (
    Service,
)

from api.models.services import (
    ServiceRequirement,
    FAQ
)


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'service']

    def create(self, validated_data):
        service_id = self.context['service_id']
        return FAQ.objects.create(service_id=service_id, **validated_data)


class ServiceSerializer(serializers.ModelSerializer):
    service_faq = FAQSerializer(read_only=True, many=True)

    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'service_faq']


class ServiceRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequirement
        fields = ['id', 'label', 'type']
        
    def create(self, validated_data):
        service_id = self.context['service_id']
        return ServiceRequirement.objects.create(service_id=service_id, **validated_data)
