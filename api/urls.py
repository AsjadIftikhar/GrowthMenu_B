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
router.register('forms', FormViewSet, basename='forms')

# Nested Routers
text_field_router = routers.NestedDefaultRouter(router, 'forms', lookup='forms')
text_field_router.register('textfield', TextFieldViewSet, basename='text-field')

image_field_router = routers.NestedDefaultRouter(router, 'forms', lookup='forms')
image_field_router.register('imagefield', ImageFieldViewSet, basename='image-field')

file_field_router = routers.NestedDefaultRouter(router, 'forms', lookup='forms')
file_field_router.register('filefield', FileFieldViewSet, basename='file-field')

order_item_router = routers.NestedDefaultRouter(router, 'orders', lookup='orders')
order_item_router.register('orderitems', OrderItemViewSet, basename='order-items')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-items')

faq_router = routers.NestedDefaultRouter(router, 'service', lookup='service')
faq_router.register('faq', FAQViewSet, basename='faq')

service_requirement_router = routers.NestedDefaultRouter(router, 'service', lookup='service')
service_requirement_router.register('requirement', ServiceRequirementViewSet, basename='service-requirement')

# URLConf
urlpatterns = (router.urls +
               service_requirement_router.urls +
               faq_router.urls +
               cart_router.urls +
               order_item_router.urls +
               text_field_router.urls +
               image_field_router.urls +
               file_field_router.urls
               )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
