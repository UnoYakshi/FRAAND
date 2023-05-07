"""Ductape solution based on https://fastapi.tiangolo.com/tutorial/security/get-current-user/."""

from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from src.fraand_core.config import settings

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """Returns a configured JWT strategy with JWT secret and a lifetime..."""

    return JWTStrategy(secret=settings.AUTH_JWT_SECRET, lifetime_seconds=3600)


jwt_bearer_auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
