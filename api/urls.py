from rest_framework_nested import routers
from api.views.order import *

router = routers.DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('carts', CartViewSet, basename='cart')

# URLConf
urlpatterns = router.urls
