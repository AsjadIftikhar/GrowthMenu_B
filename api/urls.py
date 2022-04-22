from rest_framework_nested import routers
from api.views.order import *

router = routers.DefaultRouter()
router.register('order', OrderViewSet)

# URLConf
urlpatterns = router.urls
