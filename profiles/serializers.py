from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'first_name', 'last_name', 'brand_name', 'business_category', 'phone',
                  'website_url', 'address']
