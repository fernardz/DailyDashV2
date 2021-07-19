from ..db.base_class import Base
from sqlalchemy import Boolean, Column, ForeignKey, Date, Integer, String
from sqlalchemy.orm import relationship


class Vitamin(Base):
    __tablename__ = "vitamins"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    records = relationship("VitaminRecord", back_populates="vitamin")
    goals = relationship("Vitamin_Goal", back_populates="vitamin")


class VitaminRecord(Base):
    __tablename__ = "vitamin_records"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    qty = Column(Integer, nullable=False)
    vitamin_id = Column(Integer, ForeignKey("vitamins.id"))

    vitamin = relationship("Vitamin", back_populates="records")


class Vitamin_Goal(Base):
    __tablename__ = "vitamin_goals"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    qty = Column(Integer, nullable=False)
    vitamin_id = Column(Integer, ForeignKey("vitamins.id"))

    vitamin = relationship("Vitamin", back_populates="goals")
