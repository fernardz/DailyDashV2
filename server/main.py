from fastapi import Depends, FastAPI

from server import task

app = FastAPI()

from .water import create_module as water_create
from .vitamin import create_module as vitamin_create
from .task import create_module as task_create

water_create(app)
vitamin_create(app)
task_create(app)


