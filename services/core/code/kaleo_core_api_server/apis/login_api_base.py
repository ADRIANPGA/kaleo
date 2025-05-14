# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from kaleo_core_api_server.models.default_error_response import DefaultErrorResponse
from kaleo_core_api_server.models.login_request import LoginRequest
from kaleo_core_api_server.models.login_response_body import LoginResponseBody
from kaleo_core_api_server.models.o_auth_token_request import OAuthTokenRequest


class BaseLoginApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseLoginApi.subclasses = BaseLoginApi.subclasses + (cls,)
    async def api_v1_auth_login_post(
        self,
        login_request: LoginRequest,
    ) -> LoginResponseBody:
        ...


    async def api_v1_auth_oauth_google_post(
        self,
        o_auth_token_request: OAuthTokenRequest,
    ) -> LoginResponseBody:
        ...


    async def api_v1_auth_oauth_microsoft_post(
        self,
        o_auth_token_request: OAuthTokenRequest,
    ) -> LoginResponseBody:
        ...
