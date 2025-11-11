from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(validated_token):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user = User.objects.get(id=validated_token['user_id'])
        return user
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # tenta extrair o token do header ou da query string
        headers = dict(scope['headers'])
        token = None

        if b'authorization' in headers:
            auth_header = headers[b'authorization'].decode()
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        else:
            query_string = parse_qs(scope.get("query_string", b"").decode())
            token = query_string.get("token", [None])[0]

        scope['user'] = AnonymousUser()
        if token:
            try:
                validated_token = AccessToken(token)
                user = await get_user(validated_token)
                scope['user'] = user
            except Exception:
                scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)
