from server.db.base_class import Base
from typing import List, Optional
from uuid import UUID
from datetime import date

from pydantic import BaseModel

#--------------------------#
#---VITAMIN RECORD---#


class VitaminRBase(BaseModel):
    date: date
    qty: int


class VitaminRecord(VitaminRBase):
    id: int
    vitamin_id: int

    class Config:
        orm_mode = True


class VitaminRecordCreate(VitaminRBase):
    pass

#--------------------------#
#---VITAMIN GOAL---#


class VitaminGBase(BaseModel):
    date: date
    qty: int


class VitaminGoal(VitaminGBase):
    id: int
    vitamin_id: int

    class Config:
        orm_mode = True


class VitaminGoalCreate(VitaminGBase):
    pass

#-----------------------------#
#---VITAMIN---#


class VitaminBase(BaseModel):
    name: str


class VitaminCreate(VitaminBase):
    pass


class Vitamin(VitaminBase):
    id: int
    records: List[VitaminRecord] = []
    goals: List[VitaminGoal] = []

    class Config:
        orm_mode = True

class VitaminSummary(BaseModel):
    vitamin_id: int
    name: str
    goal: Optional[int]
    amount: Optional[int]