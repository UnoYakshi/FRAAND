"""Added Items and Images (frame) models...

Revision ID: 720d958185d7
Revises: 8fc39660ddf4
Create Date: 2023-05-16 00:38:55.652063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '720d958185d7'
down_revision = '8fc39660ddf4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'items',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('items_pkey')),
    )

    op.create_table(
        'images',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('image', sa.LargeBinary(), nullable=False),
        sa.Column('item_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], name=op.f('images_item_id_fkey')),
        sa.PrimaryKeyConstraint('id', name=op.f('images_pkey')),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    op.drop_table('items')
    # ### end Alembic commands ###


def schema_upgrades():
    """schema upgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'items',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('items_pkey')),
    )

    op.create_table(
        'images',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('image', sa.LargeBinary(), nullable=False),
        sa.Column('item_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], name=op.f('images_item_id_fkey')),
        sa.PrimaryKeyConstraint('id', name=op.f('images_pkey')),
    )
    # ### end Alembic commands ###


def schema_downgrades():
    """schema downgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    op.drop_table('items')
    # ### end Alembic commands ###


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
