from pydantic import BaseModel


class AuthDetails(BaseModel):
    username: str
    password: str
    
    
class UserDetails(BaseModel):
    username: str
    password: str
    status: int
    email: str
    role: str
    mobile: str
    ref: str
    signup_ts: str
    joined: str
    class Config:
        '''Docstring here.'''
        schema_extra = {
            "example": {
                "username" : "Spanarchian",
                "password" : "Secret_Pa55w0rd",
                "status" : True,
                "email" : "spanarchian@gmail.com",
                "role" : "admin",
                "mobile" : "++447446908710",
                "ref": "7f644301-e3f1-4752-90d5-99fbfad91ab3",
                "signup_ts":"",
                "joined":""
            }
        }
        
    
    