from ..db.base_class import Base
from sqlalchemy import Boolean, Column, ForeignKey, Date, Integer, String
from sqlalchemy.orm import relationship

class Water(Base):
    __tablename__ = "water"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    size = Column(Integer)


class Water_Goal(Base):
    __tablename__ = "water_goals"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    size = Column(Integer)
