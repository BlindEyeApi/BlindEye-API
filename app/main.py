import time
import logging as logger
from fastapi import Depends, FastAPI, HTTPException
from .auth.auth import AuthHandler
from .schemas import AuthDetails, UserDetails

from .gdb.services import client
from .dependencies import get_token_header
from .internal import admin
from .routers import public, secure
import uuid


app = FastAPI()

START_TIME = time.time()
logger.info(f"Api started: {START_TIME}")

auth_handler = AuthHandler()


profiles = []
users = []

app.include_router(public.router)
app.include_router(secure.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    logger.info("Api / called")
    return {"message": "Hello Bigger Applications!", "users" : users, "profiles" : profiles}


@app.post('/register', status_code=201)
def register(user_details: UserDetails ):
    if any(x['username'] == user_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(user_details.password)
    user_id = uuid.uuid4()
    print(f"User ref = {user_id}")
    users.append({
        'username': user_details.username,
        'password': hashed_password    
    })
    user_details.password = hashed_password
    user_details.ref = uuid.uuid4()
    
    profiles.append({
        user_details.username : user_details
    })
    resp = client.register_client(user_details)
    return resp

@app.post('/login')
def login(auth_details: AuthDetails):
    logger.info(f"Api /login called: {time.time()}")
    user = None
    # Find user in dataset
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    # User NOT found in dataset
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }


@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    logger.info(f"Api /protected called: {time.time()}")
    return { 'name': username, 'profiles': profiles }



@app.get('/profile/{username}')
def profile(username):
    print(f"username supplied = {username}")
    for prof in profiles:
        print(f"prof : {prof}")
        print(f"Profile : {prof.keys()}")
        if username in prof.keys():
            return {'profile': prof }
    raise HTTPException(status_code=404, detail='Username not found')
    