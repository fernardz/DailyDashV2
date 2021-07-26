from fastapi import APIRouter, HTTPException, Depends
from typing import List

from . import schemas, crud
from sqlalchemy.orm import Session
from ..dependencies import get_db


router = APIRouter(
    prefix="/vitamins",
    tags=["vitamins"],
    responses={404: {"description": "Not found"}},
)


## Vitamins
### Vitamin Base
@router.post("/", response_model=schemas.Vitamin)
def create_vitamin(vit: schemas.VitaminCreate, db: Session = Depends(get_db)):
    return crud.create_vitamin(db=db, vit=vit)
    
@router.get("/", response_model=List[schemas.Vitamin])
def read_vitamins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vitamins = crud.get_vitamins(db, skip=skip, limit=limit)
    return vitamins

@router.get("/{vit_id}", response_model=schemas.Vitamin)
def read_vitamin(vit_id: int, db: Session = Depends(get_db)):
    db_vitamin = crud.get_vitamin(db, vit_id=vit_id)
    if db_vitamin is None:
        raise HTTPException(status_code=404, detail="Vitamin record not found")
    return db_vitamin


@router.delete("/{vit_id}", status_code=204)
def delete_vitamin(vit_id: int, db: Session = Depends(get_db)):
    db_vitamin = crud.get_vitamin(db, vit_id=vit_id)
    if db_vitamin is None:
        raise HTTPException(status_code=404, detail="Water_record not found")
    crud.delete_vitamin(db, vit_id=vit_id)

### Vitamin Records


@router.post("/record/", response_model=schemas.VitaminRecord)
def create_vitamin_record(
        vit_id: int, vit_rec: schemas.VitaminRecordCreate, db: Session = Depends(get_db)):
    return crud.create_vitamin_record(db=db, vit_rec=vit_rec, vit_id=vit_id)


@router.get("/record/", response_model=List[schemas.VitaminRecord])
def read_vitamin_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vitamin_records = crud.get_vitamin_records(db, skip=skip, limit=limit)
    return vitamin_records


@router.get("/record/{vit_rec_id}", response_model=schemas.VitaminRecord)
def read_vit_record(vit_rec_id: int, db: Session = Depends(get_db)):
    db_vit_record = crud.get_vitamin_record(db, vit_rec_id=vit_rec_id)
    if db_vit_record is None:
        raise HTTPException(status_code=404, detail="Vitamin record not found")
    return db_vit_record


@router.delete("/record/{vit_rec_id}", status_code=204)
def delete_vit_record(vit_rec_id: int, db: Session = Depends(get_db)):
    db_vit_rec = crud.get_vitamin_record(db, vit_rec_id=vit_rec_id)
    if db_vit_rec is None:
        raise HTTPException(status_code=404, detail="Vitamin Record not found")
    crud.delete_vitamin_record(db, vit_rec_id=vit_rec_id)


@router.get("/goal/", response_model=List[schemas.VitaminGoal])
def read_vitamin_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vitamin_goals = crud.get_vitamin_goals(db, skip=skip, limit=limit)
    return vitamin_goals


@router.post("/goal/", response_model=schemas.VitaminGoal)
def create_vitamin_record(
        vit_id: int, vit_goal: schemas.VitaminGoalCreate, db: Session = Depends(get_db)):
    return crud.create_vitamin_goal(db=db, vit_goal=vit_goal, vit_id=vit_id)


@router.get("/goal/first/{vit_id}", response_model=schemas.VitaminGoal)
def read_current_vitamin_goal(vit_id: int, db: Session = Depends(get_db)):
    db_vit_goal = crud.get_current_vit_goal(db, vit_id=vit_id)
    if db_vit_goal is None:
        raise HTTPException(status_code=404, detail="Vitamin Record not found")
    return db_vit_goal
