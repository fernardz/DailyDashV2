from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List

from . import schemas, crud
from sqlalchemy.orm import Session
from ..dependencies import get_db


router = APIRouter(
    prefix="/task",
    tags=["task"],
    responses={404: {"description": "Not found"}},
)


###--------------TASKS-------------------##
@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@router.post("/record", response_model=schemas.TaskRecord)
def creat_task_record(task_id: int, task_rec: schemas.TaskRecordCreate,
                      db: Session = Depends(get_db)):
 return crud.create_task_record(db=db, task_rec=task_rec, task_id=task_id)
