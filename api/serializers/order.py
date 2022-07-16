from rest_framework import serializers
from api.models.order import Order, Cart, Service, ServiceDescription, ServiceRequirement, FAQ, TextField, ImageField, Field



class ServiceDescriptionSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        service_id = self.context['service_id']
        title = self.validated_data['title']
        text = self.validated_data['text']

        try:
            # updating existing Description
            service_description = ServiceDescription.objects.get(service_id=service_id)
            service_description.title = title
            service_description.text = text
            service_description.save()
            self.instance = service_description
        except ServiceDescription.DoesNotExist:
            # Creating new description
            self.instance = ServiceDescription.objects.create(service_id=service_id, **self.validated_data)

        return self.instance

    class Meta:
        model = ServiceDescription
        service_id = serializers.IntegerField(read_only=True)
        fields = ['id', 'text']


class ServiceSerializer(serializers.ModelSerializer):
    service_description = ServiceDescriptionSerializer(read_only=True)
    class Meta:
        model = Service
        fields = ['id', 'title', 'service_description']



class OrderSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        status_category = self.validated_data['status_category']
        overall_status_category = self.validated_data['overall_status_category']

        self.instance = Order.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance
    # service = ServiceSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['service', 'status_category', 'overall_status_category', 'due_at', 'cart_id']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class ServiceRequirementSerializer(serializers.ModelSerializer):


    class Meta:
        model = ServiceRequirement
        fields = ['id', 'title', 'details', 'hint', 'type']

    # def save(self, **kwargs):
    #     print(self.validated_data)
    #     service_id = self.context['service_id']
    #     text1 = self.validated_data['text']
    #
    #
    #     try:
    #         # updating existing Description
    #         service_requirement = ServiceRequirement.objects.get(service_id=service_id)
    #         service_requirement.title = self.validated_data['title']
    #         service_requirement.details = self.validated_data['details']
    #         service_requirement.hint = self.validated_data['hint']
    #         service_requirement.save()
    #         self.instance = service_requirement
    #     except ServiceRequirement.DoesNotExist:
    #         # Creating new requirement
    #         self.instance = ServiceRequirement.objects.create(service_id=service_id, **self.validated_data)
    #
    #     return self.instance

class TextFieldSerializer(serializers.ModelSerializer):



    def create(self, validated_data):
        service_requirement_id = self.context['service_requirement_id']
        return TextField.objects.create(service_requirement_id=service_requirement_id, text=self.validated_data['text'])

    service_requirement = ServiceRequirementSerializer(read_only=True)
    class Meta:
        model = TextField

        fields = ['service_requirement', 'text']


class ImageFieldSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        service_requirement_id = self.context['service_requirement_id']
        # service_requirement = ServiceRequirement.objects.get(id = service_requirement_id)
        # service_requirement.title = self.validated_data['service_requirement']['title']
        # service_requirement.details = self.validated_data['service_requirement']['details']
        # service_requirement.hint = self.validated_data['service_requirement']['hint']
        # service_requirement.type = self.validated_data['service_requirement']['type']
        return ImageField.objects.create(service_requirement_id=service_requirement_id, upload_image=self.validated_data['upload_image'])

    service_requirement = ServiceRequirementSerializer()
    class Meta:
        model = ImageField

        fields = ['service_requirement', 'upload_image']

    # def create(self, validated_data):
    #     service_requirement_id = self.context['service_requirement_id']
    #     return ImageField.objects.create(service_requirement=service_requirement_id, **validated_data)



    # class Meta:
    #     model = ServiceRequirement
    #     fields = ['title', 'details', 'hint', 'service_id', 'type']

    # def create(self, validated_data):
    #     service_id = self.context['service_id']
    #     # print(service_id)
    #     return ServiceRequirement.objects.create(service_id=service_id, **validated_data)


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'service_description_id']

    def create(self, validated_data):
        service_description_id = self.context['service_description_id']
        return FAQ.objects.create(service_description_id=service_description_id, **validated_data)


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'




