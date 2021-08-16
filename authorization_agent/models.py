from typing import (
    Optional
)

from django.utils.translation import gettext_lazy as _
from common.provider import AuthorizationAgentProvider


class AuthorizationAgent:

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    provider: Optional[AuthorizationAgentProvider] = None

    def __init__(self, id: str, name: str, description: str='', provider: AuthorizationAgentProvider=None) -> None:
        self.id = id
        self.name = name 
        self.description = description
        self.provider = provider