from sqlalchemy.sql.selectable import subquery
from server.vitamin import models
from server.dependencies import get_db
from sqlalchemy import func
import json

db=next(get_db())

cgoal= db.query(models.Vitamin_Goal,
func.rank().over(
    order_by=models.Vitamin_Goal.date.desc(),
    partition_by=models.Vitamin_Goal.vitamin_id
).label('rnk')
).subquery()

summ = db.query(models.Vitamin, func.sum(models.VitaminRecord.qty).label('totals'))\
        .join(models.VitaminRecord).filter(models.VitaminRecord.date=='2021-08-22')\
        .group_by(models.Vitamin.id).subquery()

test=db.query(models.Vitamin.id, models.Vitamin.name, summ.c.totals, cgoal.c.qty)\
    .outerjoin(summ, models.Vitamin.id==summ.c.id)\
    .outerjoin(cgoal, models.Vitamin.id==cgoal.c.vitamin_id).\
    filter(cgoal.c.rnk==1).distinct()

for t in test:
    print(t)