from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models
from profiles.models import Customer
from django.db.models.signals import pre_save, post_init


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    placed_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField()
    STATUS = [
        ('In Progress', 'In Progress'),
        ('Awaiting Brief', 'Awaiting Brief'),
        ('In Revision', 'In Revision'),
        ('Complete', 'Complete'),
        ('Refund', 'Refund'),
        ('Canceled', 'Canceled'),
    ]
    status_category = models.CharField(choices=STATUS, default='Awaiting Brief', max_length=100)

    previous_status = None

    OVERALL_STATUS = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]
    overall_status_category = models.CharField(choices=OVERALL_STATUS, default='Active', max_length=100)


    # Detect status change
    @staticmethod
    def pre_save(sender, instance, **kwargs):
        if instance.previous_status != instance.status_category:

            # ACTIVE
            active_status_types = ['In Progress', 'Awaiting Brief', 'In Revision']

            # COMPLETED
            completed_status_types = ['Complete']

            # CANCELED
            canceled_status_types = ['Refund', 'Canceled']

            if instance.status_category in active_status_types:
                instance.overall_status_category = 'Active'
            elif instance.status_category in completed_status_types:
                instance.overall_status_category = 'Completed'
            elif instance.status_category in canceled_status_types:
                instance.overall_status_category = 'Canceled'

    @staticmethod
    def remember_state(sender, instance, **kwargs):
        instance.previous_status = instance.status_category

class Service(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    src = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    # order = models.OneToOneField(Order, on_delete=models.DO_NOTHING, null=True, related_name="service")

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="orderitems")
    # minimum quantity should be 1
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['order', 'service']]


class Form(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="forms")



# class ServiceDescription(models.Model):
#     service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name="service_description")
#
#     text = models.TextField()


class FAQ(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, related_name='service_faq')
    question = models.CharField(max_length=255, null=True)
    answer = models.CharField(max_length=1000, null=True)


class ServiceRequirement(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_requirement")
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True)

#
# class Field(models.Model):
#     class Meta:
#         abstract = True
#
#
# class TextField(Field):
#     service_requirement = models.OneToOneField(ServiceRequirement, on_delete=models.CASCADE, null=True,
#                                                related_name="text_field")
#     service_description = models.ForeignKey(ServiceDescription, on_delete=models.CASCADE, null=True,
#                                             related_name="text_field")
#     text = models.CharField(max_length=1000, null=True)
#
#
# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'user_{0}/{1}'.format(instance.user.id, filename)
#
#
# class FileField(Field):
#     service_requirement = models.OneToOneField(ServiceRequirement, on_delete=models.CASCADE, null=True,
#                                                related_name="file_field")
#     service_description = models.ForeignKey(ServiceDescription, on_delete=models.CASCADE, null=True,
#                                             related_name="file_field")
#     upload_file = models.FileField(upload_to='store/files', null=True)
#
#
# class ImageField(Field):
#     service_requirement = models.OneToOneField(ServiceRequirement, on_delete=models.CASCADE, null=True,
#                                                related_name="image_field")
#     service_description = models.ForeignKey(ServiceDescription, on_delete=models.CASCADE, null=True,
#                                             related_name="image_field")
#     upload_image = models.ImageField(upload_to='store/images', null=True)


pre_save.connect(Order.pre_save, sender=Order)
post_init.connect(Order.remember_state, sender=Order)
