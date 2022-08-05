from rest_framework_nested import routers
from api.views.cart import *
from api.views.order import *
from api.views.services import *

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('carts', CartViewSet)
router.register('service', ServiceViewSet, basename='service')

# Nested Routers
cart_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-items')

faq_router = routers.NestedDefaultRouter(router, 'service', lookup='service')
faq_router.register('faq', FAQViewSet, basename='faq')

service_requirement_router = routers.NestedDefaultRouter(router, 'service', lookup='service')
service_requirement_router.register('requirement', ServiceRequirementViewSet, basename='service-requirement')

# URLConf
urlpatterns = router.urls + service_requirement_router.urls + faq_router.urls + cart_router.urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
