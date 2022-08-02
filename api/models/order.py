from django.core.validators import MinValueValidator
from django.db import models

from profiles.models import Customer
from api.models.base import BaseTimeStampedModel
from api.models.services import Service


class Cart(BaseTimeStampedModel):
    pass


class Order(BaseTimeStampedModel):
    # todo Ali: complete the variable list
    IN_PROGRESS = 'In Progress'
    AWAITING_BRIEF = 'Awaiting Brief'

    STATUS = [
        ('In Progress', 'In Progress'),
        ('Awaiting Brief', 'Awaiting Brief'),
        ('In Revision', 'In Revision'),
        ('Complete', 'Complete'),
        ('Refund', 'Refund'),
        ('Canceled', 'Canceled'),
    ]

    # todo Ali: save method override
    MAPPINGS = {
        IN_PROGRESS: "Active"
    }
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="order")

    due_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, default="Active")
    sub_status = models.CharField(choices=STATUS, default='Awaiting Brief', max_length=100)

    def __str__(self):
        return f"{self.customer.first_name}: {self.id}"


class OrderItem(BaseTimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)

    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['order', 'service']]


class Form(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="forms")

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
