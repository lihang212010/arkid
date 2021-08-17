from typing import (
    Optional
)

from django.utils.translation import gettext_lazy as _
from common.provider import AuthFactorProvider


class AuthFactor:

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_support_registe: Optional[bool] = None
    is_support_auth:Optional[bool] = None
    provider: Optional[AuthFactorProvider] = None

    def __init__(self, id: str, name: str,is_support_registe:bool,is_support_auth:bool ,description: str='', provider: AuthFactorProvider=None) -> None:
        self.id = id
        self.name = name 
        self.is_support_registe = is_support_registe
        self.is_support_auth = is_support_auth
        self.description = description
        self.provider = provider