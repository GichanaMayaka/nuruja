"""empty message

Revision ID: fdd0e107ae31
Revises: e5bcdcd9de64
Create Date: 2023-06-15 16:07:42.528525

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'fdd0e107ae31'
down_revision = 'e5bcdcd9de64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
                    sa.Column('name', sa.String(length=20), nullable=False),
                    sa.Column('description', sa.String(length=200), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('user',
                    sa.Column('username', sa.String(length=20), nullable=False),
                    sa.Column('email', sa.String(length=120), nullable=False),
                    sa.Column('phone_number', sa.String(length=20), nullable=False),
                    sa.Column('address', sa.String(length=100), nullable=False),
                    sa.Column('is_admin', sa.Boolean(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('phone_number'),
                    sa.UniqueConstraint('username')
                    )
    op.create_table('book',
                    sa.Column('title', sa.String(length=100), nullable=False),
                    sa.Column('author', sa.String(length=120), nullable=False),
                    sa.Column('isbn', sa.String(length=120), nullable=False),
                    sa.Column('date_of_publication', sa.DateTime(), nullable=False),
                    sa.Column('status', sa.String(length=15), nullable=False),
                    sa.Column('rent_fee', sa.Integer(), nullable=False),
                    sa.Column('late_penalty_fee', sa.Integer(), nullable=False),
                    sa.Column('category_id', sa.Integer(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('isbn')
                    )
    op.create_table('shelf',
                    sa.Column('floor', sa.String(length=10), nullable=True),
                    sa.Column('book_id', sa.Integer(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('transactions',
                    sa.Column('rent_fee', sa.Float(), nullable=False),
                    sa.Column('is_return', sa.Boolean(), nullable=False),
                    sa.Column('date_borrowed', sa.DateTime(), nullable=False),
                    sa.Column('date_due', sa.DateTime(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('book_id', sa.Integer(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('user_balance',
                    sa.Column('balance', sa.Float(), nullable=False),
                    sa.Column('date_of_entry', sa.DateTime(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('transaction_id', sa.Integer(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_balance')
    op.drop_table('transactions')
    op.drop_table('shelf')
    op.drop_table('book')
    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###
