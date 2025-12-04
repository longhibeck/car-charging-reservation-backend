from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user
from src.api.models.cars import CarCreateRequest, CarResponse
from src.database import get_db
from src.models.car import Car, ConnectorType
from src.models.user import User

router = APIRouter(prefix="/cars", tags=["cars"])


@router.get("/", response_model=list[CarResponse])
async def get_cars(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get current user's cars"""
    stmt = select(Car).where(Car.user_id == current_user.id)
    result = db.execute(stmt)
    cars = result.scalars().all()
    return [CarResponse.model_validate(car) for car in cars]


@router.get("/{car_id}", response_model=CarResponse)
async def get_car(
    car_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    car = db.get(Car, car_id)

    if not car or car.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )

    return CarResponse.model_validate(car)


@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
async def create_car(
    car_data: CarCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new car for the current user"""
    try:
        connector_types = [ConnectorType(ct) for ct in car_data.connector_types]

        car = Car(
            name=car_data.name,
            connector_types=connector_types,
            battery_charge_limit=car_data.battery_charge_limit,
            battery_size=car_data.battery_size,
            max_kw_ac=car_data.max_kw_ac,
            max_kw_dc=car_data.max_kw_dc,
            user_id=current_user.id,
        )

        db.add(car)
        db.commit()
        db.refresh(car)
        return CarResponse.model_validate(car)

    except ValueError as e:
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


@router.put("/{car_id}", response_model=CarResponse)
async def update_car(
    car_id: UUID,
    car_data: CarCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an existing car"""
    try:
        car = db.get(Car, car_id)

        if not car or car.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found",
            )

        car.name = car_data.name
        car.connector_types = [ConnectorType(ct) for ct in car_data.connector_types]
        car.battery_charge_limit = car_data.battery_charge_limit
        car.battery_size = car_data.battery_size
        car.max_kw_ac = car_data.max_kw_ac
        car.max_kw_dc = car_data.max_kw_dc

        db.commit()
        db.refresh(car)

        return CarResponse.model_validate(car)

    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid connector type: {e}",
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update car",
        )


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
    car_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a car"""
    car = db.get(Car, car_id)
    if not car or car.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )

    db.delete(car)
    db.commit()
