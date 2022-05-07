from django.contrib import admin
from .models import Customer, Admin, Manager

# Register your models here.


admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(Manager)
