from django.db import models

from api.models.base import BaseTimeStampedModel


class Service(BaseTimeStampedModel):
    title = models.CharField(max_length=255)

    # todo It is a text field R&D for Rich Text/ Formatted Text
    description = models.TextField()


class FAQ(BaseTimeStampedModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, related_name='service_faq')

    question = models.CharField(max_length=255, null=True)
    answer = models.CharField(max_length=1000, null=True)


class ServiceRequirement(BaseTimeStampedModel):
    # todo Ali: Convert Type into a Model Choice Field
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_requirement")

    label = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True)
