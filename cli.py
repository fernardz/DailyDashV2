# %%
from sqlalchemy.sql.selectable import subquery
from server.vitamin import models as wmodels
from server.task import models as tmodels
from server.dependencies import get_db
from sqlalchemy import func
import json

db=next(get_db())
# %%
cgoal= db.query(wmodels.Vitamin_Goal,
func.rank().over(
    order_by=wmodels.Vitamin_Goal.date.desc(),
    partition_by=wmodels.Vitamin_Goal.vitamin_id
).label('rnk')
).subquery()

summ = db.query(wmodels.Vitamin, func.sum(wmodels.VitaminRecord.qty).label('totals'))\
        .join(wmodels.VitaminRecord).filter(wmodels.VitaminRecord.date=='2021-08-22')\
        .group_by(wmodels.Vitamin.id).subquery()

test=db.query(wmodels.Vitamin.id, wmodels.Vitamin.name, summ.c.totals, cgoal.c.qty)\
    .outerjoin(summ, wmodels.Vitamin.id==summ.c.id)\
    .outerjoin(cgoal, wmodels.Vitamin.id==cgoal.c.vitamin_id).\
    filter(cgoal.c.rnk==1).distinct()

for t in test:
    print(t)

#%%
tasks_day=db.query(tmodels.TaskRecord).filter(tmodels.TaskRecord.date=='2021-08-23').subquery()

test=db.query(tmodels.Task.desc, tasks_day.c.date, tasks_day.c.status, tasks_day.c.id)\
    .join(tasks_day, tmodels.Task.id==tasks_day.c.task_id).all()

for t in test:
    print(t)

# %%
