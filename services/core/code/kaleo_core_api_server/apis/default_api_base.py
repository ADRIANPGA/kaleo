# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from kaleo_core_api_server.models.default_error_response import DefaultErrorResponse
from kaleo_core_api_server.models.login_request import LoginRequest
from kaleo_core_api_server.models.login_response_body import LoginResponseBody
from kaleo_core_api_server.models.o_auth_token_request import OAuthTokenRequest
from kaleo_core_api_server.models.user_profile import UserProfile
from kaleo_core_api_server.security_api import get_token_BearerAuth

class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def auth_login_post(
        self,
        login_request: LoginRequest,
    ) -> LoginResponseBody:
        ...


    async def auth_oauth_google_post(
        self,
        o_auth_token_request: OAuthTokenRequest,
    ) -> LoginResponseBody:
        ...


    async def auth_oauth_microsoft_post(
        self,
        o_auth_token_request: OAuthTokenRequest,
    ) -> LoginResponseBody:
        ...


    async def users_me_get(
        self,
    ) -> UserProfile:
        ...
