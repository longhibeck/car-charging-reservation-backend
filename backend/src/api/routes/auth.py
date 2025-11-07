from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from api.models.auth import LoginRequest, LoginResponse, UserResponse
from database import get_db
from models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=LoginResponse)
async def api_login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """API endpoint for login"""
    import httpx

    from utils import create_token

    LOGIN_URL = "https://dummyjson.com/auth/login"

    try:
        # Authenticate with DummyJSON
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                LOGIN_URL,
                json={"username": login_data.username, "password": login_data.password},
            )

        if response.status_code == 200:
            data = response.json()
            external_user_id = data.get("id")
            current_username = data.get("username")

            if not external_user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid response from login service",
                )

            # Find or create user
            existing_user = (
                db.query(User).filter(User.external_user_id == external_user_id).first()
            )

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

            token = create_token(str(external_user_id))

            return LoginResponse(token=token, user=UserResponse.model_validate(user))
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
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse.model_validate(current_user)
