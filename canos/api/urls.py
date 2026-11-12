from rest_framework import routers

from canos.api.views import CanoViewSet

router = routers.SimpleRouter()
router.register("", CanoViewSet, basename="cano")
urlpatterns = router.urls
