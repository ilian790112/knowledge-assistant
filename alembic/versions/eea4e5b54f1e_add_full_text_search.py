"""add full text search

Revision ID: eea4e5b54f1e
Revises: c868a2d7500f
Create Date: 2026-07-14 21:02:23.275533
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "eea4e5b54f1e"
down_revision: Union[str, Sequence[str], None] = "c868a2d7500f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("""
        ALTER TABLE document_chunks
        ADD COLUMN search_vector tsvector
        GENERATED ALWAYS AS (
            to_tsvector('english', content)
        ) STORED;
    """)

    op.execute("""
        CREATE INDEX idx_document_chunks_search_vector
        ON document_chunks
        USING GIN (search_vector);
    """)


def downgrade() -> None:
    """Downgrade schema."""

    op.execute("""
        DROP INDEX IF EXISTS idx_document_chunks_search_vector;
    """)

    op.execute("""
        ALTER TABLE document_chunks
        DROP COLUMN search_vector;
    """)