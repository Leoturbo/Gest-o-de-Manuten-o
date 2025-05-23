"""Initial migration

Revision ID: cffb5b01c661
Revises: 
Create Date: 2025-05-15 00:36:17.813700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cffb5b01c661'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clientes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('contato', sa.String(length=100), nullable=False),
    sa.Column('endereco', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('equipamentos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('codigo', sa.String(length=20), nullable=False),
    sa.Column('descricao', sa.String(length=200), nullable=False),
    sa.Column('tipo', sa.String(length=50), nullable=False),
    sa.Column('valor_compra', sa.Float(), nullable=False),
    sa.Column('data_compra', sa.Date(), nullable=False),
    sa.Column('fornecedor', sa.String(length=100), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('equipamentos', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_equipamentos_codigo'), ['codigo'], unique=True)

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)

    op.create_table('alugueis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('equipamento_id', sa.Integer(), nullable=False),
    sa.Column('cliente_id', sa.Integer(), nullable=False),
    sa.Column('data_inicio', sa.Date(), nullable=False),
    sa.Column('data_termino', sa.Date(), nullable=False),
    sa.Column('valor', sa.Float(), nullable=False),
    sa.Column('forma_pagamento', sa.String(length=50), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('pago', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ),
    sa.ForeignKeyConstraint(['equipamento_id'], ['equipamentos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('manutencoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('equipamento_id', sa.Integer(), nullable=False),
    sa.Column('tecnico_id', sa.Integer(), nullable=True),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('problemas', sa.Text(), nullable=False),
    sa.Column('tipo', sa.String(length=20), nullable=False),
    sa.Column('custo', sa.Float(), nullable=True),
    sa.Column('proxima_manutencao', sa.Date(), nullable=True),
    sa.Column('foto_path', sa.String(length=200), nullable=True),
    sa.Column('localizacao', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['equipamento_id'], ['equipamentos.id'], ),
    sa.ForeignKeyConstraint(['tecnico_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('manutencoes')
    op.drop_table('alugueis')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_username'))
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    with op.batch_alter_table('equipamentos', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_equipamentos_codigo'))

    op.drop_table('equipamentos')
    op.drop_table('clientes')
    # ### end Alembic commands ###
