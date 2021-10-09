from fastapi import Header, HTTPException

import os
from dotenv import load_dotenv
load_dotenv()


evn_x_token = os.getenv('x_token')
evn_token = os.getenv('token')


async def get_token_header(x_token: str = Header(...)):
    print(f"evn_x_token = {evn_x_token}")
    if x_token != "Secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


# async def get_query_token(token: str):
#     if token != "jessica":
#         raise HTTPException(status_code=400, detail="No Jessica token provided")
