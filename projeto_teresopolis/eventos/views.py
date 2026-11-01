from django.utils import timezone
from rest_framework import viewsets

from .models import Evento
from .serializers import EventoSerializer


class EventoViewSet(viewsets.ModelViewSet):
    """Filtros: ?parque=<id>  e  ?proximos=1 (só eventos de hoje em diante)"""

    serializer_class = EventoSerializer

    def get_queryset(self):
        qs = Evento.objects.select_related("parque")
        parque = self.request.query_params.get("parque")
        if parque and parque.isdigit():
            qs = qs.filter(parque_id=int(parque))
        if self.request.query_params.get("proximos") in ("1", "true", "sim"):
            qs = qs.filter(data__gte=timezone.localdate())
        return qs
