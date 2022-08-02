from django.contrib import admin
from easy_select2 import select2_modelform

from api.models.order import (
    Order,
    Cart,
    Service,
)
from api.models.services import (
    FAQ,
    ServiceRequirement
)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = select2_modelform(Order, attrs={'width': '250px'})
    list_display = ["id", "customer", "due_at", "status", "sub_status"]
    list_select_related = []
    search_fields = []
    list_filter = []


admin.site.register(Cart)
admin.site.register(Service)
admin.site.register(FAQ)
admin.site.register(ServiceRequirement)
