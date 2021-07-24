from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List

from . import schemas, crud
from sqlalchemy.orm import Session
from ..dependencies import get_db

from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/water",
    tags=["water"],
    responses={404: {"description": "Not found"}},
)
# Water Consumption
@router.post("/", response_model=schemas.Water)
def create_water(water: schemas.WaterCreate, db: Session = Depends(get_db)):
    return crud.create_water(db=db, water=water)


@router.get("/", response_model=List[schemas.Water])
def read_waters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    waters = crud.get_waters(db, skip=skip, limit=limit)
    return waters


@router.get("/{water_id}", response_model=schemas.Water)
def read_water(water_id: int, db: Session = Depends(get_db)):
    db_water = crud.get_water(db, water_id=water_id)
    if db_water is None:
        raise HTTPException(status_code=404, detail="Water_record not found")
    return db_water


@router.delete("/{water_id}", status_code=204)
def delete_water(water_id: int, db: Session = Depends(get_db)):
    db_water = crud.get_water(db, water_id=water_id)
    if db_water is None:
        raise HTTPException(status_code=404, detail="Water_record not found")
    crud.delete_water(db, water_id=water_id)

# Water Goal Routes #


@router.post("/goal/", response_model=schemas.Water)
def create_water_goal(water_goal: schemas.WaterGoalCreate, db: Session = Depends(get_db)):
    return crud.create_water_goal(db=db, water_goal=water_goal)


@router.get("/goal/", response_model=List[schemas.WaterGoal])
def read_water_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    water_goals = crud.get_water_goals(db, skip=skip, limit=limit)
    return water_goals


@router.get("/goal/{water_id}", response_model=schemas.WaterGoal)
def read_water_goal(water_id: int, db: Session = Depends(get_db)):
    db_water_goal = crud.get_water_goal(db, water_id=water_id)
    if db_water_goal is None:
        raise HTTPException(status_code=404, detail="Water goal not found")
    return db_water_goal


@router.get("/goal/first/", response_model=schemas.WaterGoal)
def read_current_water_goal(db: Session = Depends(get_db)):
    water = crud.get_current_water_goal(db)
    return water
