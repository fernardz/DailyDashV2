from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server import task

app = FastAPI()

origins = [
    "http://localhost",
    "http://192.168.1.181",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://192.168.1.181:8081",
    "http://192.168.1.181:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .water import create_module as water_create
from .vitamin import create_module as vitamin_create
from .task import create_module as task_create
from .strava import create_module as strava_create

water_create(app)
vitamin_create(app)
task_create(app)
strava_create(app)


