"""create message table

Revision ID: 15c7cdc7663f
Revises:
Create Date: 2017-08-24 17:11:39.794098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15c7cdc7663f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'message',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('comment', sa.Text, nullable=False),
        sa.Column('date', sa.DateTime),
        sa.Column('comment_id', sa.Integer)
    )


def downgrade():
    op.drop_table('message')
