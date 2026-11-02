from rest_framework import routers

from .views import AlertaViewSet

router = routers.SimpleRouter()
router.register("", AlertaViewSet, basename="alerta")
urlpatterns = router.urls
