from pydantic import BaseModel, EmailStr


class AuthenticationRequest(BaseModel):
    email: EmailStr
    password: str


class AuthenticationResponse(BaseModel):
    access_token: str
    token_type: str
