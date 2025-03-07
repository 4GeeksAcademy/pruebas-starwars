"""
Corrección de migración para evitar errores de NOT NULL

Revision ID: 0f14724e9574
Revises: 3b7d6ce031d0
Create Date: 2025-03-07 12:12:11.768885
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0f14724e9574'
down_revision = '3b7d6ce031d0'
branch_labels = None
depends_on = None

def upgrade():
    # Establecer un valor por defecto en las filas donde password es NULL
    op.execute("UPDATE users SET password = 'default_password' WHERE password IS NULL")
    
    # Modificar la columna para que no acepte valores nulos
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)

def downgrade():
    # Revertir la restricción NOT NULL
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
