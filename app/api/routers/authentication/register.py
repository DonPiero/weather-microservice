from fastapi import APIRouter, HTTPException

from app.api.errors import error_409, error_500
from app.api.schemas.authentication import AuthenticationResponse, AuthenticationRequest
from app.services.authentication.login import login_user
from app.services.authentication.register import register_user


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=AuthenticationResponse)
async def register(register_parameters: AuthenticationRequest):
    try:
        success = await register_user(register_parameters.email, register_parameters.password)
        if not success:
            error_409("Account with this email already exists.")

        login_data = await login_user(register_parameters.email, register_parameters.password)

        return {"access_token": login_data, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        error_500(f"Failed registration for {register_parameters.email}, error: {e}")
