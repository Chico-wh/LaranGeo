# authentication/token_middleware_header.py
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.db import database_sync_to_async

class TokenAuthMiddlewareHeader:
    """
    Middleware para autenticar WebSocket via header Authorization: Bearer <token>
    Fallback: ?token=<token>
    Uso: TokenAuthMiddlewareHeader(URLRouter(...))
    """

    def __init__(self, inner):
        self.inner = inner
        self.jwt_auth = JWTAuthentication()

    def __call__(self, scope):
        return TokenAuthMiddlewareHeaderInstance(scope, self)

class TokenAuthMiddlewareHeaderInstance:
    def __init__(self, scope, middleware):
        self.scope = dict(scope)
        self.inner = middleware.inner
        self.jwt_auth = middleware.jwt_auth

    async def __call__(self, receive, send):
        # tenta header Authorization
        user = AnonymousUser()
        token = None

        # headers in scope are list of [name, value] as bytes
        headers = dict((k.decode().lower(), v.decode()) for k, v in self.scope.get('headers', []))
        auth_header = headers.get('authorization') or headers.get('Authorization')

        if auth_header:
            # pode vir como "Bearer <token>"
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]

        # fallback para querystring ?token=...
        if not token:
            query_string = self.scope.get('query_string', b'').decode()
            params = parse_qs(query_string)
            token_list = params.get('token', None)
            if token_list:
                token = token_list[0]

        if token:
            user = await self.get_user_from_token(token)

        self.scope['user'] = user
        inner = self.inner(self.scope)
        return await inner(receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            validated_token = self.jwt_auth.get_validated_token(token)
            user = self.jwt_auth.get_user(validated_token)
            return user
        except Exception:
            from django.contrib.auth.models import AnonymousUser
            return AnonymousUser()
