from rest_framework import serializers

from api.helpers import status_change
from api.models.order import (
    Order,
    OrderItem,
    Form,
    TextField,
    FileField,
    ImageField,
)


class TextFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextField
        fields = ['id', 'text']


class ImageFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageField
        fields = ['id', 'upload_image']


class FileFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileField
        fields = ['id', 'upload_file']


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['id', 'order_item', 'text_field', 'image_field', 'file_field']

    text_field = TextFieldSerializer(many=True, allow_null=True)
    image_field = ImageFieldSerializer(many=True, allow_null=True)
    file_field = FileFieldSerializer(many=True, allow_null=True)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'service']

    def create(self, validated_data):
        order_id = self.context['order_id']
        return OrderItem.objects.create(order_id=order_id, **validated_data)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'due_at', 'created_at', 'sub_status', 'status', 'items']

    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.CharField(max_length=20, read_only=True)

    def update(self, instance, validated_data):
        if instance.sub_status != validated_data["sub_status"]:
            validated_data["status"] = status_change(validated_data["sub_status"])
        return super(OrderSerializer, self).update(instance, validated_data)
