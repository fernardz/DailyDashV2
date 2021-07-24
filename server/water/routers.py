from fastapi.encoders import jsonable_encoder
from . import schemas, models
from ..dependencies import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import schemas, crud
from datetime import date

from fastapi import Depends

from fastapi_crudrouter import SQLAlchemyCRUDRouter


water_router=SQLAlchemyCRUDRouter(
    schema=schemas.Water,
    create_schema=schemas.WaterCreate,
    db_model=models.Water,
    db=get_db,
    prefix="water"
)

water_goal_router=SQLAlchemyCRUDRouter(
    schema=schemas.WaterGoal,
    create_schema=schemas.WaterGoalCreate,
    db_model=models.Water_Goal,
    db=get_db,
    prefix='water_goal'
)


@water_goal_router.get("/current/", response_model=schemas.WaterGoal)
def read_current_water_goal(db: Session = Depends(get_db)):
    water = crud.get_current_water_goal(db)
    return water

@water_router.get("/get_day_results/{date_id}")
def get_day_sum(date_id: date, db: Session =Depends(get_db)):
    water=db.query(models.Water).filter(models.Water.date==date_id)
    ws=water.with_entities(func.sum(models.Water.size)).scalar()
    return jsonable_encoder({'sum':ws})

    
