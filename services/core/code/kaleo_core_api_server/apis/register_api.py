# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from kaleo_core_api_server.apis.register_api_base import BaseRegisterApi
import kaleo_core_api_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from kaleo_core_api_server.models.extra_models import TokenModel  # noqa: F401
from kaleo_core_api_server.models.default_error_response import DefaultErrorResponse
from kaleo_core_api_server.models.login_response_body import LoginResponseBody
from kaleo_core_api_server.models.register_request import RegisterRequest


router = APIRouter()

ns_pkg = kaleo_core_api_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/api/v1/auth/register",
    responses={
        201: {"model": LoginResponseBody, "description": "User registered successfully"},
        400: {"model": DefaultErrorResponse, "description": "The server cannot process the request due to client error"},
        409: {"model": DefaultErrorResponse, "description": "Request conflicts with current state of the server"},
        500: {"model": DefaultErrorResponse, "description": "Server encountered an unexpected condition"},
    },
    tags=["register"],
    summary="User registration with email and password",
    response_model_by_alias=True,
)
async def api_v1_auth_register_post(
    register_request: RegisterRequest = Body(None, description=""),
) -> LoginResponseBody:
    if not BaseRegisterApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRegisterApi.subclasses[0]().api_v1_auth_register_post(register_request)
