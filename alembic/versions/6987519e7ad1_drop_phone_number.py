"""drop phone number

Revision ID: 6987519e7ad1
Revises: 6577a6ff3ca4
Create Date: 2023-02-06 18:57:39.836573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6987519e7ad1'
down_revision = '6577a6ff3ca4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users', 'phone_number')


def downgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
