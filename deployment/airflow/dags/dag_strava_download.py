# Hooks
from pydoc import ModuleScanner
from fastapi import Response
from airflow.providers.redis.hooks.redis import RedisHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.hooks.postgres_hook import PostgresHook
# Utility
from airflow.decorators import task, dag
from airflow.operators.python import get_current_context
from airflow.models import Variable
import airflow.utils.dates
# Postgres
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.automap import automap_base
from contextlib import contextmanager
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
# Additional
import json
from requests_oauthlib import OAuth2Session
from requests.models import Response as Request_Response
import logging
# Defining the dag to pull data from an api and upload
# to s3 bucket


def _get_strava_data(**_) -> Request_Response:
    """
    Download data from strava api and return data

    Returns:
        respose(str): a request response object
    """

    client_id = Variable.get("STRAVA_CLIENT")
    client_secret = Variable.get("STRAVA_CLIENT_SECRET")
    token_url = "https://www.strava.com/oauth/token"
    refresh_url = token_url

    extra = {
        'client_id': client_id,
        'client_secret': client_secret
    }

    redis_h = RedisHook(redis_conn_id='rasp-srv-redis')
    redis_client = redis_h.get_conn()

    def token_saver(token):
        token_dict = dict(token.items())
        redis_client.set('STRAVA_TOKEN', json.dumps(token_dict))

    token = redis_client.get('STRAVA_TOKEN')
    token = json.loads(token)

    logging.info(token)

    activities_url = 'https://www.strava.com/api/v3/athlete/activities?'

    try:
        client = OAuth2Session(client_id, token=token,
                               auto_refresh_kwargs=extra,
                               auto_refresh_url=refresh_url,
                               token_updater=token_saver)
        response = client.get(activities_url)
        logging.info(response)
        if response.status_code != 200:
            logging.error('FAILED API CALL TO API')
            raise ConnectionError
    except Exception as e:
        logging.critical('Could not download from API {}'.format(e))
    else:
        logging.info('Data Successfully Downloaded')
    return response


def _download_strava_to_s3(ts) -> str:
    """
    Store obtained response object into an s3 bucket
    Args:
        ts (str): time stamp to be used as key for S3 file

    Returns:
        key: S3 key pointing to file 
    """
    response = _get_strava_data()
    data = response.json()
    bucket_name = 'lifedata'
    logging.info('File name {}'.format(ts))
    key = f"stravaact/{ts}.json"

    s3_hook = S3Hook(aws_conn_id='docker-minio')
    s3_hook.load_string(
        string_data=json.dumps(data),
        key=key,
        bucket_name=bucket_name
    )
    return key


# Defining DAG to pull file from S3 and upload to
# PostgresDB
class StravaActivityCreate(BaseModel):
    """
    Pydantic class used for data validation.
    Used to validate SQL inserts into Strava Table

    Args:
        BaseModel (BaseModel): Standard pydantic Base Model
    """
    name: str
    type: str
    start_date: datetime
    distance: float
    moving_time: int
    average_speed: Optional[int] = None
    max_speed: Optional[float] = None
    average_cadence: Optional[float] = None
    average_heartrate: Optional[float] = None
    weighted_average_watts: Optional[float] = None
    kilojoules: Optional[float] = None


class StravaActivity(StravaActivityCreate):
    """
    Pydantic class used for data validation.
    Inherits from StravaActivityCreate but allows for setting
    id value.
    Set to work in orm_mode

    Args:
        StravaActivityCreate (BaseModel): Pydantic class
    """
    id: int

    class Config:
        orm_mode = True


def _upload_s3_to_db(key_name: str) -> None:
    """
    Function to download a json file from S3 and upload to PostgresDB

    Args:
        key_name (str): key pointer to S3 File in a bucket
    """
    key = key_name

    s3_hook = S3Hook(aws_conn_id='docker-minio')
    data = s3_hook.read_key(
        key,
        bucket_name='lifedata'
    )
    logging.info(data)
    data = json.loads(data)
    postgres_hook = PostgresHook(postgres_conn_id='rasp-srv-daily-dash')
    engine = postgres_hook.get_sqlalchemy_engine()
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @contextmanager
    def get_db() -> None:
        """
        Utility function to handle db session

        Yields:
            db: postgres session
        """
        db = SessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            logging.error('Could not write to DB')
            db.rollback()
            raise
        finally:
            db.close()

    with get_db() as db:
        for x in data:
            logging.info(x)
            ST = StravaActivity.parse_obj(x)
            ST_up = StravaActivityCreate.parse_obj(x)
            stmnt = insert(Base.classes.strava_activity).values(ST.dict())
            stmnt = stmnt.on_conflict_do_update(
                index_elements=['id'], set_=ST_up.dict())
            db.execute(stmnt)


@dag(
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@hourly",
    max_active_runs=1)
def strava_data_pipeline():
    """
    DAG definition for Strava API download and storage into Postgres 
    """
    @task()
    def get_data_from_strava() -> str:
        """
        Utility method for task definition
        context is used for naming conventions and must be declared in function
        definition.
        """
        context = get_current_context()
        ts_nodash = context['ts_nodash']
        key = _download_strava_to_s3(ts_nodash)
        return key

    @task()
    def upload_s3_data_to_db(key: str) -> None:
        """
        Convinience wrapper for task definition

        Args:
            key (str): Key string for S3 file
        """
        _upload_s3_to_db(key)

    key_id = get_data_from_strava()
    upload_s3_data_to_db(key_id)


# [START dag_invocation]
strava_task_dag = strava_data_pipeline()
# [END dag_invocation]
