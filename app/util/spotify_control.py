from typing import Optional

from fastapi import Request
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param


class BasicAuth(SecurityBase):
    def __init__(self, scheme_name: str = None):
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> Optional[str]:
        code: str = request.headers.get("token_info")
        scheme, param = get_authorization_scheme_param(code)
        if not code or scheme.lower() != "basic":
            return None
        return param


basic_auth = BasicAuth()
