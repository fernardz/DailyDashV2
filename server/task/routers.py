from server.task.models import TaskRecord
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List

from . import schemas, models
from sqlalchemy.orm import Session
from ..dependencies import get_db

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
