from ..db.base_class import Base
from sqlalchemy import Boolean, Column, ForeignKey, Date, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String, index=True)
    start_date = Column(Date, nullable=False)
    enabled = Column(Boolean, nullable=False, default=False)
    persist = Column(Boolean, nullable=False, default=True)
    freq = Column(String)

    records = relationship("TaskRecord", back_populates="task")


class TaskRecord(Base):
    __tablename__ = "task_records"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    status = Column(Boolean, nullable=False, default=False)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="records")
    __table_args__ = (UniqueConstraint('date', 'task_id', name='_only_one_a_day'),
                  )
