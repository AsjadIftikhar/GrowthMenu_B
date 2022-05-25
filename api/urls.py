from rest_framework_nested import routers
from api.views.order import *

from rest_framework_swagger.views import get_swagger_view
from django.urls import include, re_path




router = routers.DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')

# URLConf
# urlpatterns = router.urls
schema_view = get_swagger_view(title='GrowthMenu API')

urlpatterns = [
    re_path(r'^$', schema_view),
    re_path(r'^', include(router.urls)),
]

