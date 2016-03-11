"""empty message

Revision ID: 01d06e2e7536
Revises: None
Create Date: 2016-03-10 22:27:00.211875

"""

# revision identifiers, used by Alembic.
revision = '01d06e2e7536'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'msgTo')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('msgTo', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    ### end Alembic commands ###
