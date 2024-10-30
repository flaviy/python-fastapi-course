"""create phone number column in users table

Revision ID: e50db3791daa
Revises: 
Create Date: 2024-09-28 14:57:01.078256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e50db3791daa'
# The down_revision variable indicates the identifier of the previous revision in the migration chain. If this is the
# first migration, it is set to None. Otherwise, it would be a string representing the previous revision's
# identifier. Union[str, None] is a type hint in Python that indicates a variable can be either a string (str) or
# None. This is useful for specifying that a variable can hold a value of a specific type or be empty (i.e., None).
down_revision: Union[str, None] = None

branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(length=15), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
