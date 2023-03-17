"""empty message

Revision ID: 264971f6f4b3
Revises: 8e77270310c5
Create Date: 2023-03-17 14:12:49.928309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '264971f6f4b3'
down_revision = '8e77270310c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('disease', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('details', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.drop_column('details')
        batch_op.drop_column('disease')

    # ### end Alembic commands ###