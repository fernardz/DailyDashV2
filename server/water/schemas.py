from typing import List, Optional
from uuid import UUID
from datetime import date

from pydantic import BaseModel
#-----------------------#
#---WATER---#
class WaterBase(BaseModel):
    date: date
    size: int


class Water(WaterBase):
    id: int

    class Config:
        orm_mode = True


class WaterCreate(WaterBase):
    pass
#--------------------------#
#---WATER GOAL---#


class WaterGoal(WaterBase):
    id: int

    class Config:
        orm_mode = True


class WaterGoalCreate(WaterBase):
    pass
