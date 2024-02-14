"""Adding tokens_blacklist migration

Revision ID: 814e22de70c8
Revises: b7e6b2ed0704
Create Date: 2024-02-13 23:41:35.102619

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "814e22de70c8"
down_revision: Union[str, None] = "b7e6b2ed0704"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tokens_blacklist",
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid7()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("token", sa.String(length=512), nullable=False),
        sa.Column(
            "added_at",
            sa.Integer(),
            server_default=sa.text("extract(epoch FROM now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tokens_blacklist")
    # ### end Alembic commands ###
