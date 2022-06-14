from django.contrib import admin

from api.models.order import Order, Cart, Service, ServiceDescription, ServiceRequirement, FileField, ImageField, TextField, FAQ

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Service)
admin.site.register(ServiceDescription)
admin.site.register(FAQ)
admin.site.register(ServiceRequirement)
admin.site.register(FileField)
admin.site.register(ImageField)
admin.site.register(TextField)