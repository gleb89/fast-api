"""098yg

Revision ID: 13d488940aed
Revises: 8d51d51434a1
Create Date: 2021-01-14 22:11:56.171566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13d488940aed'
down_revision = '8d51d51434a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('images_user_id_fkey', 'images', type_='foreignkey')
    op.drop_column('images', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('images_user_id_fkey', 'images', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###