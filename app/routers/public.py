"""Public Route."""

from fastapi import APIRouter, Depends, HTTPException,Request, Form
from typing import List
from pydantic import BaseModel
from ..dependencies import get_token_header


router = APIRouter(
    prefix="/public",
    tags=["public"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_clients():
    resp = {"public" : [{"client1":"Joe Public"},{"client2":"Joey Public"},{"client3":"Jo Public"} ]}
    return resp


@router.post("/create")
async def create_client():
    resp = {"public" : [{"client1":"Joe Public"},{"client2":"Joey Public"},{"client3":"Jo Public"} ]}
    return resp
