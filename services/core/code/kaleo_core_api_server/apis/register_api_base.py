# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from kaleo_core_api_server.models.default_error_response import DefaultErrorResponse
from kaleo_core_api_server.models.login_response_body import LoginResponseBody
from kaleo_core_api_server.models.register_request import RegisterRequest


class BaseRegisterApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseRegisterApi.subclasses = BaseRegisterApi.subclasses + (cls,)
    async def api_v1_auth_register_post(
        self,
        register_request: RegisterRequest,
    ) -> LoginResponseBody:
        ...
