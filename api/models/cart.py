from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4

from api.models.base import BaseTimeStampedModel
from api.models.services import Service


class Cart(BaseTimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)


class CartItem(BaseTimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'service']]
