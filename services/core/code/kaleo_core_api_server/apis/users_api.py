# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from kaleo_core_api_server.apis.users_api_base import BaseUsersApi
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
from kaleo_core_api_server.models.user_profile import UserProfile
from kaleo_core_api_server.security_api import get_token_BearerAuth

router = APIRouter()

ns_pkg = kaleo_core_api_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/api/v1/users/me",
    responses={
        200: {"model": UserProfile, "description": "Perfil del usuario"},
        401: {"model": DefaultErrorResponse, "description": "Authentication is required or has failed"},
        403: {"model": DefaultErrorResponse, "description": "Server understood the request but refuses to authorize it"},
        404: {"model": DefaultErrorResponse, "description": "The requested resource could not be found"},
        500: {"model": DefaultErrorResponse, "description": "Server encountered an unexpected condition"},
    },
    tags=["users"],
    summary="Perfil del usuario autenticado",
    response_model_by_alias=True,
)
async def api_v1_users_me_get(
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> UserProfile:
    if not BaseUsersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseUsersApi.subclasses[0]().api_v1_users_me_get()
