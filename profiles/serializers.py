from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField()

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'brand_name', 'business_category', 'phone', 'website_url', 'address']
