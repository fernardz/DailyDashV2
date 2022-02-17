import json
import logging
import boto3
import os
from dotenv import dotenv_values
from botocore.client import Config
from botocore.client import ClientError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.automap import automap_base
from contextlib import contextmanager

from typing import Optional
from datetime import datetime

from pydantic import BaseModel

# Schema definition, since am not planning of including the whole
# module into airflow, just copied the schema from our server files
# Im sure there are cleaner ways to do so with templating


class StravaActivityCreate(BaseModel):
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
    id: int

    class Config:
        orm_mode = True


config = dotenv_values(".env")
bucket_name = 'test2'
host = 'http://localhost:9000'
filename = 'test3.json'

# Handle DB Connections
SQLALCHEMY_DATABASE_URL = os.getenv('DD_DB_HOST')
print(SQLALCHEMY_DATABASE_URL)

Base = automap_base()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
Base.prepare(engine, reflect=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


def get_data_from_s3(bucket_name, host, filename):
    s3 = boto3.resource('s3',
                        endpoint_url=host,
                        aws_access_key_id=config['S3_ACCESS_KEY'],
                        aws_secret_access_key=config['S3_SECRET'],
                        config=Config(read_timeout=0.15, connect_timeout=0.15,
                                      retries={'max_attempts': 2},
                                      signature_version='s3v4'),
                        region_name='us-east-1')
    try:
        s3.Object(bucket_name, filename).load()
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            logging.error('File does not exist')
            raise
        else:
            logging.critical('Could not connect to S3 Bucket')
            raise
    else:
        try:
            s3Bucket = s3.Bucket(bucket_name)
            s3Obj = s3Bucket.Object(filename)
            data = json.loads(s3Obj.get().get("Body").read())
        except ClientError:
            logging.critical('Something went wrong with S3')
            raise
        return data


if __name__ == "__main__":
    data = get_data_from_s3(bucket_name, host, filename)

    @contextmanager
    def get_db():
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
            ST = StravaActivity.parse_obj(x)
            ST_up = StravaActivityCreate.parse_obj(x)
            stmnt = insert(Base.classes.strava_activity).values(ST.dict())
            stmnt = stmnt.on_conflict_do_update(
                index_elements=['id'], set_=ST_up.dict())
            db.execute(stmnt)
