from typing import Any

from strawberry import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    """
    A permission class that checks if the user is authenticated.
    """

    message = "No estás autentificado. Por favor ingresa en la aplicación para tener acceso a este recurso"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        return info.context.request.user.is_authenticated
