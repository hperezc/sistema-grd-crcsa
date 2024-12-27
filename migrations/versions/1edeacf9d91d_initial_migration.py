"""Initial migration

Revision ID: 1edeacf9d91d
Revises: 
Create Date: 2024-12-26 16:46:13.184114

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1edeacf9d91d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departamento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('codigo', sa.String(length=10), nullable=True),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('municipio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('codigo', sa.String(length=10), nullable=True),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('departamento_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['departamento_id'], ['departamento.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('departamentos', schema=None) as batch_op:
        batch_op.drop_index('codigo')

    op.drop_table('departamentos')
    with op.batch_alter_table('municipios', schema=None) as batch_op:
        batch_op.drop_index('codigo')

    op.drop_table('municipios')
    with op.batch_alter_table('evaluacion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('departamento_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('municipio_id', sa.Integer(), nullable=True))
        batch_op.alter_column('empresa',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('nit',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
        batch_op.alter_column('cantidad_empleados',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
        batch_op.alter_column('responsable',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('rol',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('celular',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=120),
               type_=sa.String(length=100),
               nullable=True)
        batch_op.alter_column('sector',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.create_foreign_key(None, 'departamento', ['departamento_id'], ['id'])
        batch_op.create_foreign_key(None, 'municipio', ['municipio_id'], ['id'])
        batch_op.drop_column('departamento')
        batch_op.drop_column('ciudad')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('evaluacion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ciudad', mysql.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('departamento', mysql.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('sector',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('celular',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
        batch_op.alter_column('rol',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('responsable',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('cantidad_empleados',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.alter_column('nit',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
        batch_op.alter_column('empresa',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.drop_column('municipio_id')
        batch_op.drop_column('departamento_id')

    op.create_table('municipios',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('codigo', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('nombre', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('departamento_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['departamento_id'], ['departamentos.id'], name='municipios_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('municipios', schema=None) as batch_op:
        batch_op.create_index('codigo', ['codigo'], unique=True)

    op.create_table('departamentos',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('codigo', mysql.VARCHAR(length=2), nullable=True),
    sa.Column('nombre', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('departamentos', schema=None) as batch_op:
        batch_op.create_index('codigo', ['codigo'], unique=True)

    op.drop_table('municipio')
    op.drop_table('departamento')
    # ### end Alembic commands ###
