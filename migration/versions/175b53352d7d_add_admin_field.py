"""Add admin field

Revision ID: 175b53352d7d
Revises: 5fcd4f779a6a
Create Date: 2021-11-07 18:49:21.530306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "175b53352d7d"
down_revision = "5fcd4f779a6a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "students",
        sa.Column(
            "is_admin",
            sa.Boolean(),
            nullable=True,
            default=True,
        ),
    )
    op.execute("UPDATE students SET is_admin = false;")
    op.alter_column("students", "is_admin", nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("students", "is_admin")
    # ### end Alembic commands ###
