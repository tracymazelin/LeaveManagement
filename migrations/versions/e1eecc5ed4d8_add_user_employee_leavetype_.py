"""add user, employee, leaveType, approvalStatus tables

Revision ID: e1eecc5ed4d8
Revises: 
Create Date: 2022-04-04 23:29:10.704706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1eecc5ed4d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('approval_status',
    sa.Column('approval_status_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('deleted_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('approval_status_id')
    )
    op.create_index(op.f('ix_approval_status_created_date'), 'approval_status', ['created_date'], unique=False)
    op.create_index(op.f('ix_approval_status_deleted_date'), 'approval_status', ['deleted_date'], unique=False)
    op.create_index(op.f('ix_approval_status_updated_date'), 'approval_status', ['updated_date'], unique=False)
    op.create_table('leave_type',
    sa.Column('leave_type_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('days_per_year', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('deleted_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('leave_type_id')
    )
    op.create_index(op.f('ix_leave_type_created_date'), 'leave_type', ['created_date'], unique=False)
    op.create_index(op.f('ix_leave_type_deleted_date'), 'leave_type', ['deleted_date'], unique=False)
    op.create_index(op.f('ix_leave_type_updated_date'), 'leave_type', ['updated_date'], unique=False)
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('deleted_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_created_date'), 'user', ['created_date'], unique=False)
    op.create_index(op.f('ix_user_deleted_date'), 'user', ['deleted_date'], unique=False)
    op.create_index(op.f('ix_user_updated_date'), 'user', ['updated_date'], unique=False)
    op.create_table('employee',
    sa.Column('employee_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=60), nullable=False),
    sa.Column('last_name', sa.String(length=60), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('deleted_date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('employee_id')
    )
    op.create_index(op.f('ix_employee_deleted_date'), 'employee', ['deleted_date'], unique=False)
    op.create_index(op.f('ix_employee_first_name'), 'employee', ['first_name'], unique=False)
    op.create_index(op.f('ix_employee_last_name'), 'employee', ['last_name'], unique=False)
    op.create_index(op.f('ix_employee_updated_date'), 'employee', ['updated_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_employee_updated_date'), table_name='employee')
    op.drop_index(op.f('ix_employee_last_name'), table_name='employee')
    op.drop_index(op.f('ix_employee_first_name'), table_name='employee')
    op.drop_index(op.f('ix_employee_deleted_date'), table_name='employee')
    op.drop_table('employee')
    op.drop_index(op.f('ix_user_updated_date'), table_name='user')
    op.drop_index(op.f('ix_user_deleted_date'), table_name='user')
    op.drop_index(op.f('ix_user_created_date'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_leave_type_updated_date'), table_name='leave_type')
    op.drop_index(op.f('ix_leave_type_deleted_date'), table_name='leave_type')
    op.drop_index(op.f('ix_leave_type_created_date'), table_name='leave_type')
    op.drop_table('leave_type')
    op.drop_index(op.f('ix_approval_status_updated_date'), table_name='approval_status')
    op.drop_index(op.f('ix_approval_status_deleted_date'), table_name='approval_status')
    op.drop_index(op.f('ix_approval_status_created_date'), table_name='approval_status')
    op.drop_table('approval_status')
    # ### end Alembic commands ###