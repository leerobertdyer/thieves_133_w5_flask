"""added team table and relationships

Revision ID: 0259d52d4849
Revises: 7f70e2fccfa3
Create Date: 2023-11-15 13:18:07.744697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0259d52d4849'
down_revision = '7f70e2fccfa3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('player', sa.Integer(), nullable=True),
    sa.Column('pokemon', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['player'], ['user.id'], ),
    sa.ForeignKeyConstraint(['pokemon'], ['pokemon.name'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team')
    # ### end Alembic commands ###
