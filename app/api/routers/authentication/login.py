from fastapi import APIRouter, HTTPException

from app.api.errors import error_401, error_500
from app.api.schemas.authentication import AuthenticationResponse, AuthenticationRequest
from app.services.authentication.login import login_user


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=AuthenticationResponse)
async def login(login_parameters: AuthenticationRequest):
    try:
        login_data = await login_user(login_parameters.email, login_parameters.password)
        if not login_data:
            error_401("Login failed. Please try again.")

        return {"access_token": login_data, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        error_500(f"Failed login for {login_parameters.email}, error: {e}")
