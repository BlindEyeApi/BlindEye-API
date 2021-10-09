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
        
    
    