from rest_framework.routers import SimpleRouter

from .views import TrilhaViewSet

router = SimpleRouter()
router.register("trilhas", TrilhaViewSet, basename="trilha")

urlpatterns = router.urls
