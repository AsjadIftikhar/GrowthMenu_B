from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    """Growth Menu Customer Model"""

    # Brand Name
    brand_name = models.CharField(max_length=255)

    # Business Category Drop Down
    AGENCY = "Agency"
    EB = "Ecommerce Business"
    AM = "Affiliate Marketing"
    TB = "Tech Business"
    OTHER = "Other"

    CATEGORIES = [
        (AGENCY, 'Agency'),
        (EB, 'Ecommerce Business'),
        (AM, 'Affiliate Marketing'),
        (TB, 'Tech Business'),
        (OTHER, 'Other'),

    ]
    business_category = models.CharField(choices=CATEGORIES, default=AGENCY, max_length=100)

    # Phone Number
    phone = models.CharField(max_length=255)

    # Website URL
    website_url = models.URLField()

    # Address
    address = models.CharField(max_length=255)

    # Link to default user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
