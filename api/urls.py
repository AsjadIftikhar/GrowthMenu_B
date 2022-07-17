from rest_framework_nested import routers
from api.views.order import *

router = routers.DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('carts', CartViewSet, basename='cart')
router.register('service', ServiceViewSet, basename='service')
# router.register('service_description', ServiceDescriptionViewSet, basename='description')
# router.register('service_requirement', ServiceRequirementViewSet, basename='requirement')

service_description_router = routers.NestedDefaultRouter(router, 'service', lookup='service')
service_description_router.register('description', ServiceDescriptionViewSet, basename='service-description')

# service_requirement_router = routers.NestedDefaultRouter(router, 'service', lookup='service')
# service_requirement_router.register('requirement', ServiceRequirementViewSet, basename='service-requirement')

service_requirement_router = routers.NestedDefaultRouter(router, 'service', lookup='service')
service_requirement_router.register('requirement', ServiceRequirementViewSet, basename='service-requirement')

faq_router = routers.NestedDefaultRouter(service_description_router, 'description', lookup='description')
faq_router.register('faq', ServiceRequirementViewSet, basename='faq')

# URLConf
urlpatterns = router.urls + service_description_router.urls + service_requirement_router.urls + faq_router.urls
