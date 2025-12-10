import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user
from src.api.models.auth import (
    LoginRequest,
    LoginResponse,
    UserResponse,
)
from src.database import get_db
from src.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])

logger = logging.getLogger(__name__)


@router.post("/login", response_model=LoginResponse)
async def api_login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """API endpoint for login"""

    LOGIN_URL = "https://dummyjson.com/user/login"

    try:
        # Authenticate with DummyJSON
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                LOGIN_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "username": login_data.username,
                    "password": login_data.password,
                    "expiresInMins": 30,
                },
            )

        if response.status_code == 200:
            data = response.json()
            external_user_id = data.get("id")
            current_username = data.get("username")
            access_token = data.get("accessToken")
            refresh_token = data.get("refreshToken")

            if not external_user_id or not access_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid response from login service",
                )

            # Find or create user
            stmt = select(User).where(User.external_user_id == external_user_id)
            existing_user = db.scalars(stmt).first()

            if not existing_user:
                new_user = User(
                    external_user_id=external_user_id, username=current_username
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                user = new_user
            else:
                if existing_user.username != current_username:
                    existing_user.username = current_username
                    db.commit()
                user = existing_user

            # Try to validate and catch the specific error
            try:
                user_response = UserResponse.model_validate(user)
                logger.info(f"UserResponse validation successful: {user_response}")
            except Exception as validation_error:
                logger.error(f"UserResponse validation failed: {validation_error}")
                # Return error details for debugging
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"User validation failed: {str(validation_error)}",
                )

            return LoginResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                user=user_response,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to login service",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}",
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse.model_validate(current_user)
