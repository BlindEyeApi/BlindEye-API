from fastapi import Depends, FastAPI, HTTPException
from .auth.auth import AuthHandler
from .schemas import AuthDetails, UserDetails


from .dependencies import get_token_header
from .internal import admin
from .routers import public, secure


app = FastAPI()

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
    return {"message": "Hello Bigger Applications!", "users" : users}


@app.post('/register', status_code=201)
def register(user_details: UserDetails):
    if any(x['username'] == user_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(user_details.password)
    # Add user to dataset
    users.append({
        'username': user_details.username,
        'password': hashed_password    
    })
    profiles.append({
        "username":user_details
    })

    return


@app.post('/login')
def login(auth_details: AuthDetails):
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
    return { 'name': username, 'profiles': profiles }