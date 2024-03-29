"""Tool form databse added

Revision ID: a2e6913ca0a1
Revises: 114f8237346a
Create Date: 2022-04-08 11:49:19.856221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2e6913ca0a1'
down_revision = '114f8237346a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('submissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('secondary_id', sa.Integer(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('dogs_breed', sa.String(length=128), nullable=False),
    sa.Column('dogs_name', sa.String(length=128), nullable=False),
    sa.Column('dogs_dob', sa.Date(), nullable=False),
    sa.Column('dogs_sex', sa.String(length=128), nullable=False),
    sa.Column('dogs_neutered', sa.String(length=128), nullable=False),
    sa.Column('scratching', sa.String(length=128), nullable=False),
    sa.Column('scratching_site', sa.String(length=128), nullable=False),
    sa.Column('scratching_triggers', sa.String(length=128), nullable=False),
    sa.Column('vocalising_when_scratching', sa.String(length=128), nullable=False),
    sa.Column('nibbling_licking', sa.String(length=128), nullable=False),
    sa.Column('vocalisation_yelping_or_screaming', sa.String(length=128), nullable=False),
    sa.Column('vocalisation_yelping_or_screaming_text_box', sa.String(length=128), nullable=False),
    sa.Column('exercise', sa.String(length=128), nullable=False),
    sa.Column('play', sa.String(length=128), nullable=False),
    sa.Column('stairs_jumping', sa.String(length=128), nullable=False),
    sa.Column('interactions', sa.String(length=128), nullable=False),
    sa.Column('interactions_text_box', sa.String(length=128), nullable=False),
    sa.Column('sleep', sa.String(length=128), nullable=False),
    sa.Column('other_signs', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submissions')
    # ### end Alembic commands ###
