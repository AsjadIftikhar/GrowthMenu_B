from django.db import models
from profiles.models import Customer


# Create your models here.
class Order(models.Model):
    categories = [
        ('Product Descriptions', 'Product Descriptions'),
        ('Blogs & Articles', 'Blogs & Articles'),
        ('Email Marketing', 'Email Marketing'),
        ('Ad Copy', 'Ad Copy'),
        ('Web Copy', 'Web Copy'),
        ('Video Scripts', 'Video Scripts')
    ]
    category = models.CharField(choices=categories, max_length=255)
    placed_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateField()
    requirements = models.CharField(max_length=2000)
    details = models.CharField(max_length=2000)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
