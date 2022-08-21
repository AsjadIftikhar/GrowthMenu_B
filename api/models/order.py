from django.core.validators import MinValueValidator
from django.db import models

from profiles.models import Customer
from api.models.base import BaseTimeStampedModel
from api.models.services import Service


class Order(BaseTimeStampedModel):
    # todo Ali: complete the variable list
    IN_PROGRESS = 'In Progress'
    AWAITING_BRIEF = 'Awaiting Brief'
    IN_REVISION = 'In Revision'
    COMPLETE = 'Complete'
    REFUND = 'Refund'
    CANCELED = 'Canceled'

    STATUS = [
        (IN_PROGRESS, IN_PROGRESS),
        (AWAITING_BRIEF, AWAITING_BRIEF),
        (IN_REVISION, IN_REVISION),
        (COMPLETE, COMPLETE),
        (REFUND, REFUND),
        (CANCELED, CANCELED),
    ]

    # todo Ali: save method override: Done

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="order")

    due_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, default="Active")
    sub_status = models.CharField(choices=STATUS, default=AWAITING_BRIEF, max_length=100)

    # def __str__(self):
    #     return f"{self.customer.first_name}: {self.id}"


class OrderItem(BaseTimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)


class Form(models.Model):
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name="forms")


class TextField(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=True, related_name="text_field")
    text = models.CharField(max_length=1000, null=True)


# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'user_{0}/{1}'.format(instance.user.id, filename)


class FileField(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=True, related_name="file_field")
    upload_file = models.FileField(upload_to='store/files', null=True)


class ImageField(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=True, related_name="image_field")
    upload_image = models.ImageField(upload_to='store/images', null=True)
