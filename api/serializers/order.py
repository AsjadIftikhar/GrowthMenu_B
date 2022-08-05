from rest_framework import serializers

from api.helpers import status_change
from api.models.order import (
    Order,
    OrderItem,
)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'service', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'due_at', 'created_at', 'sub_status', 'status', 'items']

    def update(self, instance, validated_data):
        if instance.sub_status != validated_data["sub_status"]:
            validated_data["status"] = status_change(validated_data["sub_status"])
        return super(OrderSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        # todo Whatever
        return super(OrderSerializer, self).create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

#
# class TextFieldSerializer(serializers.ModelSerializer):
#
#     def update(self, instance, validated_data):
#         text_field = TextField.objects.get(service_requirement_id=self.context["service_requirement_id"])
#         text_field.service_requirement.pk = self.context["service_requirement_id"]
#         text_field.text = self.validated_data['text']
#         text_field.save()
#         self.instance = ServiceRequirement.objects.get(id=self.context["service_requirement_id"])
#         return self.instance
#
#     class Meta:
#         model = TextField
#         service_requirement_id = serializers.IntegerField(read_only=True)
#         fields = ['text', 'service_requirement_id']
#
#
# class ImageFieldSerializer(serializers.ModelSerializer):
#
#     def update(self, instance, validated_data):
#         image_field = ImageField.objects.get(service_requirement_id=self.context["service_requirement_id"])
#         image_field.upload_image = self.validated_data['upload_image']
#         image_field.save()
#         self.instance = ServiceRequirement.objects.get(id=self.context["service_requirement_id"])
#         return self.instance
#
#     class Meta:
#         model = ImageField
#         service_requirement_id = serializers.IntegerField(read_only=True)
#         fields = ['upload_image', 'service_requirement_id']
#
#
# class FileFieldSerializer(serializers.ModelSerializer):
#
#     def update(self, instance, validated_data):
#         file_field = FileField.objects.get(service_requirement_id=self.context["service_requirement_id"])
#         file_field.service_requirement.pk = self.context["service_requirement_id"]
#         file_field.upload_file = self.validated_data['upload_file']
#         file_field.save()
#         self.instance = ServiceRequirement.objects.get(id=self.context["service_requirement_id"])
#         return self.instance
#
#     class Meta:
#         model = FileField
#         service_requirement_id = serializers.IntegerField(read_only=True)
#         fields = ['upload_file', 'service_requirement_id']
