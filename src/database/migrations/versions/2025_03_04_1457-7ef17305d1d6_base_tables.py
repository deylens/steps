"""Base tables

Revision ID: 7ef17305d1d6
Revises: 71c80f084a54
Create Date: 2025-03-04 14:57:05.702457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ef17305d1d6'
down_revision: Union[str, None] = '71c80f084a54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('skill_types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_skill_types_name'), 'skill_types', ['name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telegram_id')
    )
    op.create_table('children',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('skills',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('skill_type_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('criteria', sa.Text(), nullable=False),
    sa.Column('recommendation', sa.Text(), nullable=False),
    sa.Column('age_start', sa.Integer(), nullable=False),
    sa.Column('age_end', sa.Integer(), nullable=False),
    sa.Column('age_actual', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['skill_type_id'], ['skill_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('diagnosis_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('skill_id', sa.Integer(), nullable=False),
    sa.Column('skill_type_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('mastered', sa.Boolean(), nullable=False),
    sa.Column('child_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['child_id'], ['children.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ),
    sa.ForeignKeyConstraint(['skill_type_id'], ['skill_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('diagnosis_result',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('child_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('skill_types_id', sa.Integer(), nullable=False),
    sa.Column('age_assessment', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['child_id'], ['children.id'], ),
    sa.ForeignKeyConstraint(['skill_types_id'], ['skill_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('diagnosis_result')
    op.drop_table('diagnosis_history')
    op.drop_table('skills')
    op.drop_table('children')
    op.drop_table('users')
    op.drop_index(op.f('ix_skill_types_name'), table_name='skill_types')
    op.drop_table('skill_types')
    # ### end Alembic commands ###
