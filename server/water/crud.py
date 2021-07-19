from sqlalchemy.orm import Session

from . import models, schemas
from ..dependencies import get_db

##### Water CRUD
def get_waters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Water).offset(skip).limit(limit).all()


def create_water(db: Session, water: schemas.WaterCreate):
    db_water = models.Water(date=water.date, size=water.size)
    db.add(db_water)
    db.commit()
    db.refresh(db_water)
    return db_water


def get_water(db: Session, water_id: int):
    return db.query(models.Water).filter(models.Water.id == water_id).first()


def delete_water(db: Session, water_id: int):
    water_rec = db.query(models.Water).filter(
        models.Water.id == water_id).first()
    db.delete(water_rec)
    db.commit()

#### Water Goal CRUD


def get_water_goals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Water_Goal).offset(skip).limit(limit).all()


def create_water_goal(db: Session, water_goal: schemas.WaterGoalCreate):
    db_water = models.Water_Goal(date=water_goal.date, size=water_goal.size)
    db.add(db_water)
    db.commit()
    db.refresh(db_water)
    return db_water


def get_water_goal(db: Session, wg_id: int):
    return db.query(models.Water_Goal).filter(models.Water_Goal.id == wg_id).first()


def delete_water_goal(db: Session, wg_id: int):
    wg_rec = db.query(models.Water_Goal).filter(
        models.Water_Goal.id == wg_id).first()
    db.delete(wg_rec)
    db.commit()


def get_current_water_goal(db: Session):
    return db.query(models.Water_Goal).order_by(models.Water_Goal.date.desc()).first()
