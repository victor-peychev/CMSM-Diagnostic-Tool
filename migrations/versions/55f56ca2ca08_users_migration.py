"""Users migration

Revision ID: 55f56ca2ca08
Revises: 
Create Date: 2022-04-08 09:24:58.156227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55f56ca2ca08'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('dogs_name', sa.String(length=128), nullable=False))
    op.add_column('users', sa.Column('dogs_breed', sa.String(length=128), nullable=False))
    op.add_column('users', sa.Column('dogs_dob', sa.Date(), nullable=False))
    op.add_column('users', sa.Column('dogs_sex', sa.String(length=128), nullable=False))
    op.add_column('users', sa.Column('dogs_neutered', sa.String(length=128), nullable=False))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'dogs_neutered')
    op.drop_column('users', 'dogs_sex')
    op.drop_column('users', 'dogs_dob')
    op.drop_column('users', 'dogs_breed')
    op.drop_column('users', 'dogs_name')
    # ### end Alembic commands ###