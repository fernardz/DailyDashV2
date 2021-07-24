from sqlalchemy.orm import Session

from . import models, schemas
from ..dependencies import get_db

####--------------TASKS-----------###

"""
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def create_task_record(db: Session,
                       task_rec: schemas.TaskRecordCreate, task_id: int):
    db_record = models.TaskRecord(**task_rec.dict(), task_id=task_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
"""

