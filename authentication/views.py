from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterMotoristaSerializer, MotoristaProfileSerializer
from transporte.models import Motorista

class RegisterMotoristaView(generics.CreateAPIView):
    serializer_class = RegisterMotoristaSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        motorista = serializer.save()

        user = motorista.user
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Motorista registrado com sucesso.",
            "user": user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


class MotoristaProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MotoristaProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Motorista.objects.get(user=self.request.user)
