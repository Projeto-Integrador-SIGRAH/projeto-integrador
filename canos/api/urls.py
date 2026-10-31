from rest_framework import routers
from .views import CanoViewSet

router = routers.SimpleRouter()
router.register(r'canos', CanoViewSet, basename='cano')
urlpatterns = router.urls