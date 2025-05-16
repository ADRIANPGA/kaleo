# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from fastapi import Security

from kaleo_core_api_server.models.default_error_response import DefaultErrorResponse
from kaleo_core_api_server.models.user_profile import UserProfile
from kaleo_core_api_server.security_api import get_token_BearerAuth
from kaleo_core_api_server.models.extra_models import TokenModel
class BaseUsersApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseUsersApi.subclasses = BaseUsersApi.subclasses + (cls,)
    async def api_v1_users_me_get(
        self,
        token_BearerAuth: TokenModel = Security(
            get_token_BearerAuth
        ),
    ) -> UserProfile:
        ...
