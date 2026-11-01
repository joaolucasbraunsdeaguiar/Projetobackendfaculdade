from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("parques.urls")),
    path("api/", include("trilhas.urls")),
    path("api/", include("eventos.urls")),
    path("api/", include("avisos.urls")),
    path("api/", include("usuarios.urls")),
]
