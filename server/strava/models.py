from sqlalchemy.sql.sqltypes import BigInteger
from ..db.base_class import Base
from sqlalchemy import Column, Float, String, DateTime


class StravaActivity (Base):
    __tablename__ = "strava_activity"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    distance = Column(Float, nullable=False)
    moving_time = Column(BigInteger, nullable=False)
    average_speed = Column(Float)
    max_speed = Column(Float)
    average_cadence = Column(Float)
    average_heartrate = Column(Float)
    weighted_average_watts = Column(Float)
    kilojoules = Column(Float)
