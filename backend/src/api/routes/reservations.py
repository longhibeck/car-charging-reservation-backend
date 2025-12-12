from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user
from src.api.models.reservations import ReservationCreateRequest, ReservationResponse
from src.database import get_db
from src.models.car import Car
from src.models.reservation import Reservation
from src.models.user import User
from src.services.charging_point import charging_point_service

router = APIRouter(prefix="/reservations", tags=["reservations"])


async def check_charging_point_availability(charging_point_id: str) -> dict:
    """Check if charging point is available (external API + existing reservations)"""

    # 1. Check external API for charging point status
    charging_point = await charging_point_service.get_charging_point(charging_point_id)

    if not charging_point:
        return {"available": False, "reason": "Charging point not found"}

    # 2. Check if charging point is operationally available
    if charging_point.status != "available":
        return {
            "available": False,
            "reason": f"Charging point is {charging_point.status}",
        }

    # 3. Check for overlapping reservations in our database
    ## later

    return {
        "available": True,
        "reason": None,
        "charging_point": charging_point,
    }


@router.post(
    "/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED
)
async def create_reservation(
    reservation_data: ReservationCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new charging reservation"""

    # Get car and validate ownership in one step
    stmt = select(Car).where(Car.id == reservation_data.car_id)
    result = db.execute(stmt)
    car = result.scalar_one_or_none()

    if not car or car.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Car not found")

    # Simple validation (no external API for now)
    now = datetime.now(timezone.utc)
    if reservation_data.start_time <= now:
        raise HTTPException(status_code=400, detail="Start time must be in the future")

    duration = reservation_data.end_time - reservation_data.start_time
    duration_hours = duration.total_seconds() / 3600

    if duration_hours < 0.25:
        raise HTTPException(status_code=400, detail="Minimum 15 minutes")
    if duration_hours > 12:
        raise HTTPException(status_code=400, detail="Maximum 12 hours")

    # Check charging point availability
    availability_check = await check_charging_point_availability(
        reservation_data.charging_point_id,
    )

    if not availability_check["available"]:
        raise HTTPException(
            status_code=409,  # Conflict
            detail=f"Charging point is not available during the requested time. {availability_check['reason']}",
        )

    # Create reservation with both user_id and car_id
    try:
        reservation = Reservation(
            start_time=reservation_data.start_time,
            end_time=reservation_data.end_time,
            charging_point_id=reservation_data.charging_point_id,
            user_id=current_user.id,
            car_id=car.id,
        )
        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        return ReservationResponse.model_validate(reservation)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to create reservation: {str(e)}"
        )


@router.get("/", response_model=list[ReservationResponse])
async def get_reservations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current user's reservations"""

    # Direct query instead of user.reservations
    stmt = select(Reservation).where(Reservation.user_id == current_user.id)
    reservations = db.scalars(stmt).all()

    return [ReservationResponse.model_validate(r) for r in reservations]
