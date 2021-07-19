from typing import List, Optional
from uuid import UUID
from datetime import date

from pydantic import BaseModel

#-----------------------------------------#
#---TASK RECORD---#


class TaskRBase(BaseModel):
    date: date
    status: bool


class TaskRecord(TaskRBase):
    id: int
    task_id: int

    class Config:
        orm_mode = True


class TaskRecordCreate(TaskRBase):
    pass

#---TASK---#


class TaskBase(BaseModel):
    desc: str
    start_date: date
    enabled: bool
    freq: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    records: List[TaskRecord] = []

    class Config:
        orm_mode = True
