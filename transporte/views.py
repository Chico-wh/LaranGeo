from rest_framework import viewsets, permissions
from .models import Linha, Ponto, Motorista, Localizacao
from .serializers import LinhaSerializer, PontoSerializer, MotoristaSerializer, LocalizacaoSerializer

# --- VIEWSETS ---

class LinhaViewSet(viewsets.ModelViewSet):
    queryset = Linha.objects.all()
    serializer_class = LinhaSerializer
    permission_classes = [permissions.AllowAny]  # público (passageiro)

class PontoViewSet(viewsets.ModelViewSet):
    queryset = Ponto.objects.all()
    serializer_class = PontoSerializer
    permission_classes = [permissions.AllowAny]  # público (passageiro)

class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = [permissions.IsAuthenticated]  # apenas motorista autenticado

class LocalizacaoViewSet(viewsets.ModelViewSet):
    queryset = Localizacao.objects.all()
    serializer_class = LocalizacaoSerializer

    def get_permissions(self):
        # Passageiros podem ver; motoristas autenticados podem criar
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
