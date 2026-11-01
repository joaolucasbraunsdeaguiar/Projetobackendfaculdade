from rest_framework import viewsets

from .models import Trilha
from .serializers import TrilhaSerializer


class TrilhaViewSet(viewsets.ModelViewSet):
    """Filtros: ?parque=<id>  e  ?em_manutencao=true|false"""

    serializer_class = TrilhaSerializer

    def get_queryset(self):
        qs = Trilha.objects.select_related("parque")
        parque = self.request.query_params.get("parque")
        if parque and parque.isdigit():
            qs = qs.filter(parque_id=int(parque))
        manutencao = self.request.query_params.get("em_manutencao")
        if manutencao is not None:
            qs = qs.filter(em_manutencao=manutencao.lower() in ("1", "true", "sim"))
        return qs
