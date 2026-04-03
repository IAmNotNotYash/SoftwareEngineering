"""Add commerce models: products, product_images, cart_items, orders, order_items, order_tracking_events

Revision ID: a1b2c3d4e5f6
Revises: 30f6bb4684bf
Create Date: 2026-04-03 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '30f6bb4684bf'
branch_labels = None
depends_on = None


def upgrade():
    # --- products ---
    op.create_table(
        'products',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('artist_id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('materials', sa.Text(), nullable=True),
        sa.Column('dimensions', sa.String(length=200), nullable=True),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('in_stock', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['artist_id'], ['artist_profiles.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    # --- product_images ---
    op.create_table(
        'product_images',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('product_id', sa.String(length=36), nullable=False),
        sa.Column('image_url', sa.String(length=500), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    # --- cart_items ---
    op.create_table(
        'cart_items',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('buyer_id', sa.String(length=36), nullable=False),
        sa.Column('product_id', sa.String(length=36), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('added_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['buyer_id'], ['buyer_profiles.id']),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('buyer_id', 'product_id', name='uq_cart_buyer_product'),
    )

    # --- orders ---
    op.create_table(
        'orders',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('buyer_id', sa.String(length=36), nullable=False),
        sa.Column('artist_id', sa.String(length=36), nullable=False),
        sa.Column(
            'status',
            sa.Enum('pending', 'processing', 'shipped', 'delivered', 'cancelled',
                    name='order_status_enum'),
            nullable=False,
            server_default='pending',
        ),
        sa.Column('subtotal', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('shipping_cost', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('shipping_address_snapshot', sa.JSON(), nullable=False),
        sa.Column('payment_snapshot', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['buyer_id'], ['buyer_profiles.id']),
        sa.ForeignKeyConstraint(['artist_id'], ['artist_profiles.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    # --- order_items ---
    op.create_table(
        'order_items',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('order_id', sa.String(length=36), nullable=False),
        sa.Column('product_id', sa.String(length=36), nullable=True),  # nullable: survives soft-delete
        sa.Column('product_title_snapshot', sa.String(length=200), nullable=False),
        sa.Column('product_image_snapshot', sa.String(length=500), nullable=True),
        sa.Column('artist_name_snapshot', sa.String(length=150), nullable=False),
        sa.Column('price_at_purchase', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id']),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    # --- order_tracking_events ---
    op.create_table(
        'order_tracking_events',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('order_id', sa.String(length=36), nullable=False),
        sa.Column(
            'event',
            sa.Enum('confirmed', 'dispatched', 'out_for_delivery', 'delivered', 'cancelled',
                    name='tracking_event_enum'),
            nullable=False,
        ),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('order_tracking_events')
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('cart_items')
    op.drop_table('product_images')
    op.drop_table('products')

    # Drop custom enum types (PostgreSQL-specific)
    op.execute("DROP TYPE IF EXISTS order_status_enum")
    op.execute("DROP TYPE IF EXISTS tracking_event_enum")
