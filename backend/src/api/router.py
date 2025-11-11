from fastapi import APIRouter

from api.routes.auth import router as auth_router
from api.routes.cars import router as cars_router

# Main API router that combines all sub-routers with versioning
router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
    responses={
        200: {"description": "Success"},
        201: {"description": "Created"},
        204: {"description": "No Content - Successfully removed"},
        404: {"description": "Not found"},
        401: {"description": "Unauthorized - Invalid or missing authentication"},
        422: {"description": "Validation Error - Invalid request data"},
        500: {"description": "Internal Server Error"},
    },
)

# Include all route modules
router.include_router(auth_router)
router.include_router(cars_router)
