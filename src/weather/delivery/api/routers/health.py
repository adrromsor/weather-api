from datetime import datetime, timezone

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))
