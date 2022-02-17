from typing import Optional
from datetime import datetime

from pydantic import BaseModel

# ---------------------------------#
# ----STRAVA-------#


class StravaActivityCreate(BaseModel):
    name: str
    type: str
    start_date: datetime
    distance: float
    moving_time: int
    average_speed: Optional[int] = None
    max_speed: Optional[float] = None
    average_cadence: Optional[float] = None
    average_heartrate: Optional[float] = None
    weighted_average_watts: Optional[float] = None
    kilojoules: Optional[float] = None


class StravaActivity(StravaActivityCreate):
    id: int

    class Config:
        orm_mode = True
