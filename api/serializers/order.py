from rest_framework import serializers
from api.models.order import Order, Cart, Service, ServiceDescription, ServiceRequirement, FAQ, TextField, ImageField, FileField


class ServiceDescriptionSerializer(serializers.ModelSerializer):

    # def save(self, **kwargs):
    #     service_id = self.context['service_id']
    #     text = self.validated_data['text']
    #
    #     try:
    #         # updating existing Description
    #         service_description = ServiceDescription.objects.get(service_id=service_id)
    #         service_description.text = text
    #         service_description.save()
    #         self.instance = service_description
    #     except ServiceDescription.DoesNotExist:
    #         # Creating new description
    #         self.instance = ServiceDescription.objects.create(service_id=service_id, **self.validated_data)
    #
    #     return self.instance

    def create(self, validated_data):
        service_id = self.context['service_id']
        return ServiceDescription.objects.create(service_id=service_id, **validated_data)

    class Meta:
        model = ServiceDescription
        service_id = serializers.IntegerField(read_only=True)
        fields = ['id', 'text', 'service_id']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        service_id = serializers.IntegerField(read_only=True)
        fields = ['id', 'question', 'answer', 'service_id']

    def create(self, validated_data):
        service_id = self.context['service_id']
        return FAQ.objects.create(service_id=service_id, **validated_data)

class ServiceSerializer(serializers.ModelSerializer):
    service_description = ServiceDescriptionSerializer(read_only=True)
    service_faq = FAQSerializer(read_only=True, many=True)

    class Meta:
        model = Service
        fields = ['id', 'title', 'src', 'service_description', 'service_faq']


class OrderSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        status_category = self.validated_data['status_category']
        overall_status_category = self.validated_data['overall_status_category']

        self.instance = Order.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    service = ServiceSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['service', 'status_category', 'overall_status_category', 'due_at', 'cart_id']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class TextFieldSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        text_field = TextField.objects.get(service_requirement_id=self.context["service_requirement_id"])
        text_field.service_requirement.pk = self.context["service_requirement_id"]
        text_field.text = self.validated_data['text']
        text_field.save()
        self.instance = ServiceRequirement.objects.get(id=self.context["service_requirement_id"])
        return self.instance

    class Meta:
        model = TextField
        service_requirement_id = serializers.IntegerField(read_only=True)
        fields = ['text', 'service_requirement_id']


class ImageFieldSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        image_field = ImageField.objects.get(service_requirement_id=self.context["service_requirement_id"])
        image_field.upload_image = self.validated_data['upload_image']
        image_field.save()
        self.instance = ServiceRequirement.objects.get(id=self.context["service_requirement_id"])
        return self.instance

    class Meta:
        model = ImageField
        service_requirement_id = serializers.IntegerField(read_only=True)
        fields = ['upload_image', 'service_requirement_id']


class FileFieldSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        file_field = FileField.objects.get(service_requirement_id=self.context["service_requirement_id"])
        file_field.service_requirement.pk = self.context["service_requirement_id"]
        file_field.upload_file = self.validated_data['upload_file']
        file_field.save()
        self.instance = ServiceRequirement.objects.get(id=self.context["service_requirement_id"])
        return self.instance

    class Meta:
        model = FileField
        service_requirement_id = serializers.IntegerField(read_only=True)
        fields = ['upload_file', 'service_requirement_id']

class ServiceRequirementSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        service_id = self.context['service_id']
        label = self.validated_data['label']

        type = self.validated_data['type']

        self.instance = ServiceRequirement.objects.create(service_id=service_id, label=label, type=type)

        if type == 'textField':
            text_field = TextField.objects.create(service_requirement_id=self.instance.pk, text=self.context['text'])
            text_field.save()
        if type == 'imageField':
            image_field = ImageField.objects.create(service_requirement_id=self.instance.pk, upload_image=self.context['upload_image'])
            image_field.save()
        if type == 'fileField':
            file_field = FileField.objects.create(service_requirement_id=self.instance.pk, upload_file=self.context['upload_file'])
            file_field.save()

        return self.instance

    text_field = TextFieldSerializer(read_only=True)
    image_field = ImageFieldSerializer(read_only=True)
    file_field = FileFieldSerializer(read_only=True)
    class Meta:
        model = ServiceRequirement
        fields = ['id', 'label', 'type', 'text_field', 'image_field', 'file_field']




