from fastapi import Depends, FastAPI
from .db import Base

app = FastAPI()

from .water import create_module as water_create

water_create(app)


