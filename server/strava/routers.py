from . import schemas, models
from ..dependencies import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date

from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter

strava_router=SQLAlchemyCRUDRouter(
    schema=schemas.StravaActivity,
    create_schema=schemas.StravaActivityCreate,
    db_model=models.StravaActivity,
    db=get_db,
    prefix="strava"
)

@strava_router.get("/get_day_results/{date_id}")
def get_day_sum(date_id: date, db: Session = Depends(get_db)):
    act=db.query(models.StravaActivity) \
        .filter(func.DATE(models.StravaActivity.start_date)==date_id)
    acts_sum=act.with_entities(func.sum(models.StravaActivity.distance).label('distance'),
    func.sum(models.StravaActivity.moving_time).label('time')).one()
    if acts_sum is None:
        return jsonable_encoder({'distance': 0, 'time': 0})
    else:
        return jsonable_encoder({'distance': acts_sum.distance, 'time':acts_sum.time})
