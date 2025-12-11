import os

import httpx
from pydantic import BaseModel

from src.models.car import ConnectorType


class ChargingPoint(BaseModel):
    id: str
    name: str
    connector_type: ConnectorType
    charging_type: str
    max_power_kw: int
    status: str


class ChargingPointService:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or os.getenv(
            "CHARGING_POINTS_URL", "http://localhost:8081"
        )

    async def get_charging_point(self, charging_point_id: str) -> ChargingPoint | None:
        """Get charging point status from external API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/charging-points/{charging_point_id}"
                )
                response.raise_for_status()
                data = response.json()
                return ChargingPoint(**data)
            except httpx.HTTPError:
                return None


# Singleton instance
charging_point_service = ChargingPointService()
