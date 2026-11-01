from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ContatoView, ParqueViewSet

router = SimpleRouter()
router.register("parques", ParqueViewSet)

urlpatterns = router.urls + [
    path("contato/", ContatoView.as_view(), name="contato"),
]
