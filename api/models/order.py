from datetime import datetime

from django.db import models
from profiles.models import Customer
from django.db.models.signals import pre_save, post_init


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
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
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=True)


class ServiceDescription(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name="service_description")
    title = models.CharField(max_length=255)
    details = models.TextField()


class FAQ(models.Model):
    service_description = models.ForeignKey(ServiceDescription, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=255, null=True)
    answer = models.CharField(max_length=1000, null=True)


class ServiceRequirement(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_requirement")
    title = models.CharField(max_length=255)
    details = models.TextField()
    hint = models.CharField(max_length=255)


class Field(models.Model):
    service_requirement = models.OneToOneField(ServiceRequirement, on_delete=models.CASCADE)
    service_description = models.ForeignKey(ServiceDescription, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class TextField(Field):
    text = models.CharField(max_length=1000)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class FileField(Field):
    upload_file = models.FileField(upload_to=user_directory_path)


class ImageField(Field):
    upload_image = models.ImageField(upload_to=user_directory_path)






pre_save.connect(Order.pre_save, sender=Order)
post_init.connect(Order.remember_state, sender=Order)

#
# # Create your models here.
# class Order(models.Model):
#     categories = [
#         ('Product Descriptions', 'Product Descriptions'),
#         ('Blogs & Articles', 'Blogs & Articles'),
#         ('Email Marketing', 'Email Marketing'),
#         ('Ad Copy', 'Ad Copy'),
#         ('Web Copy', 'Web Copy'),
#         ('Video Scripts', 'Video Scripts')
#     ]
#     category = models.CharField(choices=categories, max_length=255)
#
#     # IN_PROGRESS = "In Progress"
#     # AWAITING_BRIEF = "Awaiting Brief"
#     # IN_REVISION = "In Revision"
#     # REFUND = "Refund"
#     # CANCELED = "Canceled"
#
#     STATUS = [
#         ('In Progress', 'In Progress'),
#         ('Awaiting Brief', 'Awaiting Brief'),
#         ('In Revision', 'In Revision'),
#         ('Complete', 'Complete'),
#         ('Refund', 'Refund'),
#         ('Canceled', 'Canceled'),
#     ]
#     status_category = models.CharField(choices=STATUS, default='Awaiting Brief', max_length=100)
#     previous_status = None
#
#     OVERALL_STATUS = [
#         ('Active', 'Active'),
#         ('Completed', 'Completed'),
#         ('Canceled', 'Canceled'),
#     ]
#     overall_status_category = models.CharField(choices=OVERALL_STATUS, default='Active', max_length=100)
#
#     # active True by default
#     active = True
#     completed = False
#     canceled = False
#
#     placed_at = models.DateTimeField(auto_now_add=True)
#     due_at = models.DateField()
#     requirements = models.TextField(max_length=2000)
#     details = models.TextField(max_length=2000)
#
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return "[{}] Order Placed by - {} > due at {}".format(self.category, self.customer, self.due_at)
#
#     # Detect status change
#     @staticmethod
#     def pre_save(sender, instance, **kwargs):
#         if instance.previous_status != instance.status_category:
#
#             # ACTIVE
#             active_status_types = ['In Progress', 'Awaiting Brief', 'In Revision']
#
#             # COMPLETED
#             completed_status_types = ['Complete']
#
#             # CANCELED
#             canceled_status_types = ['Refund', 'Canceled']
#
#             if instance.status_category in active_status_types:
#                 instance.overall_status_category = 'Active'
#             elif instance.status_category in completed_status_types:
#                 instance.overall_status_category = 'Completed'
#             elif instance.status_category in canceled_status_types:
#                 instance.overall_status_category = 'Canceled'
#
#     @staticmethod
#     def remember_state(sender, instance, **kwargs):
#         instance.previous_status = instance.status_category
#
#
# pre_save.connect(Order.pre_save, sender=Order)
# post_init.connect(Order.remember_state, sender=Order)
