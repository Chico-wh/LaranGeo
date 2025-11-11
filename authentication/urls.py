from django.urls import path
from .views import RegisterMotoristaView, MotoristaProfileView

urlpatterns = [
    path('signup/', RegisterMotoristaView.as_view(), name='motorista_signup'),
    path('profile/', MotoristaProfileView.as_view(), name='motorista_profile'),

]
