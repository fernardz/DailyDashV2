from . import schemas, models
from ..dependencies import get_db

from fastapi_crudrouter import SQLAlchemyCRUDRouter

strava_router=SQLAlchemyCRUDRouter(
    schema=schemas.StravaActivity,
    create_schema=schemas.StravaActivityCreate,
    db_model=models.StravaActivity,
    db=get_db,
    prefix="strava"
)