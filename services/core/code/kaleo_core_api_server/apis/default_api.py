# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from kaleo_core_api_server.apis.default_api_base import BaseDefaultApi
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
from kaleo_core_api_server.models.login_request import LoginRequest
from kaleo_core_api_server.models.login_response_body import LoginResponseBody
from kaleo_core_api_server.models.o_auth_token_request import OAuthTokenRequest
from kaleo_core_api_server.models.user_profile import UserProfile
from kaleo_core_api_server.security_api import get_token_BearerAuth

router = APIRouter()

ns_pkg = kaleo_core_api_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/auth/login",
    responses={
        200: {"model": LoginResponseBody, "description": "Login exitoso"},
        400: {"model": DefaultErrorResponse, "description": "The server cannot process the request due to client error"},
        401: {"model": DefaultErrorResponse, "description": "Authentication is required or has failed"},
        500: {"model": DefaultErrorResponse, "description": "Server encountered an unexpected condition"},
    },
    tags=["default"],
    summary="Login tradicional con usuario/contraseña",
    response_model_by_alias=True,
)
async def auth_login_post(
    login_request: LoginRequest = Body(None, description=""),
) -> LoginResponseBody:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().auth_login_post(login_request)


@router.post(
    "/auth/oauth/google",
    responses={
        200: {"model": LoginResponseBody, "description": "Login exitoso"},
        400: {"model": DefaultErrorResponse, "description": "The server cannot process the request due to client error"},
        401: {"model": DefaultErrorResponse, "description": "Authentication is required or has failed"},
        500: {"model": DefaultErrorResponse, "description": "Server encountered an unexpected condition"},
    },
    tags=["default"],
    summary="Login con token de Google",
    response_model_by_alias=True,
)
async def auth_oauth_google_post(
    o_auth_token_request: OAuthTokenRequest = Body(None, description=""),
) -> LoginResponseBody:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().auth_oauth_google_post(o_auth_token_request)


@router.post(
    "/auth/oauth/microsoft",
    responses={
        200: {"model": LoginResponseBody, "description": "Login exitoso"},
        400: {"model": DefaultErrorResponse, "description": "The server cannot process the request due to client error"},
        401: {"model": DefaultErrorResponse, "description": "Authentication is required or has failed"},
        500: {"model": DefaultErrorResponse, "description": "Server encountered an unexpected condition"},
    },
    tags=["default"],
    summary="Login con token de Microsoft",
    response_model_by_alias=True,
)
async def auth_oauth_microsoft_post(
    o_auth_token_request: OAuthTokenRequest = Body(None, description=""),
) -> LoginResponseBody:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().auth_oauth_microsoft_post(o_auth_token_request)


@router.get(
    "/users/me",
    responses={
        200: {"model": UserProfile, "description": "Perfil del usuario"},
        401: {"model": DefaultErrorResponse, "description": "Authentication is required or has failed"},
        403: {"model": DefaultErrorResponse, "description": "Server understood the request but refuses to authorize it"},
        404: {"model": DefaultErrorResponse, "description": "The requested resource could not be found"},
        500: {"model": DefaultErrorResponse, "description": "Server encountered an unexpected condition"},
    },
    tags=["default"],
    summary="Perfil del usuario autenticado",
    response_model_by_alias=True,
)
async def users_me_get(
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> UserProfile:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().users_me_get()
