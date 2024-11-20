"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create id_searches table (note the plural form)
    op.create_table(
        'id_searches',  # Changed from id_search to id_searches
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_number', sa.String(length=13), nullable=False),
        sa.Column('date_of_birth', sa.DateTime(), nullable=False),
        sa.Column('gender', sa.String(length=10), nullable=False),
        sa.Column('citizen', sa.Boolean(), nullable=False),
        sa.Column('search_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id_number')
    )

    # Create holidays table (note the plural form)
    op.create_table(
        'holidays',  # Changed from holiday to holidays
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_search_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['id_search_id'], ['id_searches.id'], ),  # Updated reference
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index(op.f('ix_id_searches_id_number'), 'id_searches', ['id_number'], unique=True)
    op.create_index(op.f('ix_holidays_id_search_id'), 'holidays', ['id_search_id'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_holidays_id_search_id'), table_name='holidays')
    op.drop_index(op.f('ix_id_searches_id_number'), table_name='id_searches')

    # Drop tables
    op.drop_table('holidays')
    op.drop_table('id_searches')
