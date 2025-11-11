from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LinhaViewSet, PontoViewSet, MotoristaViewSet, LocalizacaoViewSet

router = DefaultRouter()
router.register('linhas', LinhaViewSet)
router.register('pontos', PontoViewSet)
router.register('motoristas', MotoristaViewSet)
router.register('localizacoes', LocalizacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
