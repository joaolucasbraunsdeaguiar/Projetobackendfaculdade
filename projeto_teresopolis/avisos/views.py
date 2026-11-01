from rest_framework import viewsets

from .models import Aviso
from .serializers import AvisoSerializer


class AvisoViewSet(viewsets.ModelViewSet):
    """Público vê só avisos ativos; funcionários veem todos. Filtro: ?parque=<id>"""

    serializer_class = AvisoSerializer

    def get_queryset(self):
        qs = Aviso.objects.select_related("parque", "trilha")
        user = self.request.user
        if not (user.is_authenticated and user.is_staff):
            qs = qs.filter(ativo=True)
        parque = self.request.query_params.get("parque")
        if parque and parque.isdigit():
            qs = qs.filter(parque_id=int(parque))
        return qs
