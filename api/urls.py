from rest_framework_nested import routers
from api.views.order import *
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('carts', CartViewSet, basename='cart')
router.register('service', ServiceViewSet, basename='service')

service_description_router = routers.NestedDefaultRouter(router, 'service', lookup='service')
service_description_router.register('description', ServiceDescriptionViewSet, basename='service-description')

faq_router = routers.NestedDefaultRouter(router, 'service', lookup='service')
faq_router.register('faq', FAQViewSet, basename='faq')

service_requirement_router = routers.NestedDefaultRouter(router, 'service', lookup='service')
service_requirement_router.register('requirement', ServiceRequirementViewSet, basename='service-requirement')


# URLConf
urlpatterns = router.urls + service_description_router.urls + service_requirement_router.urls + faq_router.urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

