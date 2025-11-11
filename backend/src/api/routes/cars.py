from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from api.models.cars import CarCreateRequest, CarResponse
from database import get_db
from models.car import Car, Connector, ConnectorType
from models.user import User

router = APIRouter(prefix="/cars", tags=["cars"])


@router.get("/")
async def get_cars(current_user: User = Depends(get_current_user)):
    """Get current user's cars"""
    cars = [CarResponse.model_validate(car) for car in current_user.cars]
    return {"cars": cars}


@router.post("/", response_model=CarResponse)
async def create_car(
    car_data: CarCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new car for the current user"""
    try:
        # Create the car
        new_car = Car(
            name=car_data.name,
            battery_charge_limit=car_data.battery_charge_limit,
            battery_size=car_data.battery_size,
            max_kw_ac=car_data.max_kw_ac,
            max_kw_dc=car_data.max_kw_dc,
            user_id=current_user.id,
        )
        db.add(new_car)
        db.flush()

        # Create connectors
        for ctype in car_data.connector_types:
            connector = Connector(
                type=ConnectorType[ctype],
                car_id=new_car.id,
            )
            db.add(connector)

        db.commit()
        db.refresh(new_car)

        return CarResponse.model_validate(new_car)

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid connector type: {e}",
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create car",
        )
