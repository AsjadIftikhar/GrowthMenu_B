from rest_framework_nested import routers
from api.views.order import *

router = routers.DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('carts', CartViewSet, basename='cart')
router.register('service', ServiceViewSet, basename='service')
router.register('service_description', ServiceDescriptionViewSet, basename='description')
router.register('service_requirement', ServiceRequirementViewSet, basename='requirement')

# URLConf
urlpatterns = router.urls
