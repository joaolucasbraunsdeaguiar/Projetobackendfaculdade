from rest_framework.routers import SimpleRouter

from .views import AvisoViewSet

router = SimpleRouter()
router.register("avisos", AvisoViewSet, basename="aviso")

urlpatterns = router.urls
