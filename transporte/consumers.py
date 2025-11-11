# transporte/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.cache import cache
from .models import Localizacao, Motorista, Linha
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async
from django.utils import timezone
import datetime

RATE_LIMIT_SECONDS = 1  # mínimo entre updates por motorista (ajuste conforme necessário)

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.linha_codigo = self.scope['url_route']['kwargs'].get('linha_codigo')
        self.global_group = "locations"
        await self.channel_layer.group_add(self.global_group, self.channel_name)
        if self.linha_codigo:
            self.line_group = f"linha_{self.linha_codigo}"
            await self.channel_layer.group_add(self.line_group, self.channel_name)
        else:
            self.line_group = None

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.global_group, self.channel_name)
        if self.line_group:
            await self.channel_layer.group_discard(self.line_group, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # passageiros (não autenticados) não enviam updates
        try:
            data = json.loads(text_data)
        except Exception:
            return

        user = self.scope.get('user', None)
        if user is None or getattr(user, "is_anonymous", True):
            await self.send(json.dumps({"error": "not_authenticated"}))
            return

        motorista = await self.get_motorista_for_user(user)
        if motorista is None:
            await self.send(json.dumps({"error": "user_not_motorista"}))
            return

        # rate limit simple per motorista id using cache
        if not await self.check_rate_limit(motorista.id):
            await self.send(json.dumps({"error": "rate_limited"}))
            return

        latitude = data.get('latitude')
        longitude = data.get('longitude')
        linha_codigo = data.get('linha') or self.linha_codigo or (motorista.linha_atual.codigo if motorista.linha_atual else None)

        # Optional: enforce that linha_codigo must match motorista.linha_atual (if you want)
        if motorista.linha_atual and linha_codigo and linha_codigo != motorista.linha_atual.codigo:
            # se preferir, rejeite; aqui apenas notifica
            await self.send(json.dumps({"warning": "linha_mismatch", "expected": motorista.linha_atual.codigo, "received": linha_codigo}))

        loc = await self.create_localizacao(motorista, latitude, longitude)
        username = await self.get_motorista_username(motorista)

        event = {
            "motorista":username,
            "motorista_id": motorista.id,
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": loc.timestamp.isoformat(),
            "linha": linha_codigo,
        }
        

       
        # broadcast global
        await self.channel_layer.group_send(self.global_group, {
            "type": "broadcast.message",
            "message": event
        })

        # broadcast por linha
        if linha_codigo:
            await self.channel_layer.group_send(f"linha_{linha_codigo}", {
                "type": "broadcast.message",
                "message": event
            })

    async def broadcast_message(self, event):
        message = event.get('message')
        await self.send(text_data=json.dumps(message))
    @database_sync_to_async
    def get_motorista_username(self, motorista):
        return motorista.user.username

    @database_sync_to_async
    def get_motorista_for_user(self, user):
        try:
            return Motorista.objects.get(user=user)
        except Motorista.DoesNotExist:
            return None

    @database_sync_to_async
    def create_localizacao(self, motorista, latitude, longitude):
        loc = Localizacao.objects.create(
            motorista=motorista,
            latitude=latitude,
            longitude=longitude
        )
        return loc

    @database_sync_to_async
    def check_rate_limit(self, motorista_id):
        """
        Retorna True se permitido; aplica cooldown em cache.
        """
        key = f"loc_rate_{motorista_id}"
        last = cache.get(key)
        now = timezone.now().timestamp()
        if last and now - float(last) < RATE_LIMIT_SECONDS:
            return False
        cache.set(key, now, timeout=RATE_LIMIT_SECONDS + 1)
        return True
