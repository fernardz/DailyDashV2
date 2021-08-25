from server.task.models import TaskRecord
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List

from . import schemas, models
from sqlalchemy.orm import Session
from ..dependencies import get_db

from datetime import date

from fastapi_crudrouter import SQLAlchemyCRUDRouter


task_record_router = SQLAlchemyCRUDRouter(
    schema=schemas.TaskRecord,
    create_schema=schemas.TaskRecordCreate,
    db_model=models.TaskRecord,
    db=get_db,
    prefix='task_record'
)

task_router = SQLAlchemyCRUDRouter(
    schema=schemas.Task,
    create_schema=schemas.TaskCreate,
    db_model=models.Task,
    db=get_db,
    prefix='task'
)

@task_record_router.get("/day/{tdate}", response_model=List[schemas.DailyTask])
def get_day_tasks(tdate: date, db: Session=Depends(get_db)):
    tasks_day = db.query(models.TaskRecord).filter(
        models.TaskRecord.date == tdate ).subquery()

    tasks = db.query(models.Task.id.label('task_id'),\
        models.Task.desc, tasks_day.c.date, tasks_day.c.status, tasks_day.c.id)\
        .join(tasks_day, models.Task.id == tasks_day.c.task_id).all()
    
    print(tasks)
    return tasks

