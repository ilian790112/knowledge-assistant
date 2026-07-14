"""add vector embedding

Revision ID: c868a2d7500f
Revises: 670131999757
Create Date: 2026-07-11 15:33:49.911621
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "c868a2d7500f"
down_revision: Union[str, Sequence[str], None] = "670131999757"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add the embedding column
    op.add_column(
        "document_chunks",
        sa.Column(
            "embedding",
            Vector(384),
            nullable=True,
        ),
    )

    # Recreate FK with CASCADE delete
    op.drop_constraint(
        "document_chunks_document_id_fkey",
        "document_chunks",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "document_chunks_document_id_fkey",
        "document_chunks",
        "documents",
        ["document_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "document_chunks_document_id_fkey",
        "document_chunks",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "document_chunks_document_id_fkey",
        "document_chunks",
        "documents",
        ["document_id"],
        ["id"],
    )

    op.drop_column(
        "document_chunks",
        "embedding",
    )