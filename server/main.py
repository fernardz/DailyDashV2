from fastapi import Depends, FastAPI

app = FastAPI()

from .water import create_module as water_create
from .vitamin import create_module as vitamin_create

water_create(app)
vitamin_create(app)


