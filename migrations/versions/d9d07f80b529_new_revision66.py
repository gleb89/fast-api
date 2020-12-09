"""New revision66

Revision ID: d9d07f80b529
Revises: 2896a2b84175
Create Date: 2020-12-04 10:48:16.514566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9d07f80b529'
down_revision = '2896a2b84175'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('rating_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'rating', ['rating_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'rating_id')
    # ### end Alembic commands ###