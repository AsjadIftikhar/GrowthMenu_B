from django.contrib import admin
from easy_select2 import select2_modelform

from api.models.cart import (
    Cart,
)
from api.models.order import (
    Order,
)
from api.models.services import (
    Service,
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


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = select2_modelform(Order, attrs={'width': '250px'})
    list_display = ["id", "title"]
    list_select_related = []
    search_fields = []
    list_filter = []


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    form = select2_modelform(Order, attrs={'width': '250px'})
    list_display = ["id", "question"]
    list_select_related = []
    search_fields = []
    list_filter = []


@admin.register(ServiceRequirement)
class ServiceRequirementAdmin(admin.ModelAdmin):
    form = select2_modelform(Order, attrs={'width': '250px'})
    list_display = ["id", "service", "label", "type"]
    list_select_related = []
    search_fields = []
    list_filter = []


admin.site.register(Cart)

