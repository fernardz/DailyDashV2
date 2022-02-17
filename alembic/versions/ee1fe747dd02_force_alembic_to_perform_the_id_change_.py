"""Force Alembic to perform the id change to BigInt

Revision ID: ee1fe747dd02
Revises: 448c1e6a79a5
Create Date: 2022-02-17 12:56:18.879423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee1fe747dd02'
down_revision = '448c1e6a79a5'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('strava_activity', 'id', nullable=False, type_=sa.BigInteger)
    op.create_index('ix_strava_activity_id',
                    'strava_activity', ['id'], unique=True)
    pass


def downgrade():
    op.alter_column('strava_activity','id',type_=sa.Integer, nullable=False)
    op.drop_index('ix_strava_activity_id', table_name='strava_activity')
    pass
