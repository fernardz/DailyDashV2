from sqlalchemy.orm import Session

from . import models, schemas
from ..dependencies import get_db


### Vitamin Crud
def get_vitamins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vitamin).offset(skip).limit(limit).all()


def get_vitamin(db: Session, vit_id: int):
    return db.query(models.Vitamin).filter(models.Vitamin.id == vit_id).first()


def delete_vitamin(db: Session, vit_id: int):
    vit_rec = db.query(models.Vitamin).filter(
        models.Vitamin.id == vit_id).first()
    db.delete(vit_rec)
    db.commit()


def create_vitamin(db: Session, vit: schemas.VitaminCreate):
    db_vit = models.Vitamin(name=vit.name)
    db.add(db_vit)
    db.commit()
    db.refresh(db_vit)
    return db_vit


def create_vitamin_record(db: Session,
                          vit_rec: schemas.VitaminRecordCreate, vit_id: id):
    db_record = models.VitaminRecord(**vit_rec.dict(), vitamin_id=vit_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_vitamin_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.VitaminRecord).offset(skip).limit(limit).all()


def get_vitamin_record(db: Session, vit_rec_id: int):
    return db.query(models.VitaminRecord).filter(models.VitaminRecord.id == vit_rec_id).first()


def delete_vitamin_record(db: Session, vit_rec_id: int):
    vit_rec = db.query(models.VitaminRecord).filter(
        models.VitaminRecord.id == vit_rec_id).first()
    db.delete(vit_rec)
    db.commit()


### Vitamin Goals
def get_vitamin_goals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vitamin_Goal).offset(skip).limit(limit).all()


def create_vitamin_goal(db: Session,
                        vit_goal: schemas.VitaminGoalCreate, vit_id: int):
    db_vgoal = models.Vitamin_Goal(**vit_goal.dict(), vitamin_id=vit_id)
    db.add(db_vgoal)
    db.commit()
    db.refresh(db_vgoal)
    return db_vgoal


def get_vit_goal(db: Session, vg_id: int):
    return db.query(models.Water_Goal).filter(models.Vitamin_Goal.id == vg_id).first()


def delete_vit_goal(db: Session, vg_id: int):
    water_rec = db.query(models.Water_Goal).filter(
        models.Vitamin_Goal.id == vg_id).first()
    db.delete(water_rec)
    db.commit()


def get_current_vit_goal(db: Session, vit_id: int):
    return db.query(models.Vitamin_Goal).filter(
        models.Vitamin_Goal.vitamin_id == vit_id).order_by(
        models.Vitamin_Goal.date.desc()).first()
