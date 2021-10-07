"""Secure Route."""

from fastapi import APIRouter, Depends, HTTPException,Request, Form
from typing import List
from pydantic import BaseModel
from ..dependencies import get_token_header


router = APIRouter(
    prefix="/secure",
    tags=["secure"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_clients():
    resp = {"public" : [{"client1":"Secret Jack"},{"client2":"Steve Secure"},{"client3":"Seal Secure"} ]}
    return resp
