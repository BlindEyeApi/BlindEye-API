"""Secure Route."""

from fastapi import APIRouter, Depends, HTTPException,Request, Form
from typing import List
from pydantic import BaseModel
from ..dependencies import get_token_header
from ..auth.auth import AuthHandler
from ..schemas import AuthDetails



router = APIRouter(
    prefix="/secure",
    tags=["secure"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

auth_handler = AuthHandler()

@router.get("/")
async def get_clients(username=Depends(auth_handler.auth_wrapper)):
    resp = { "user" : username}
    return resp
