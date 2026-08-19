from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship

from app.db import Base

# Output dimension of all-MiniLM-L6-v2 (see DECISIONS_LOG D003). If the embedding model
# ever changes, this constant and the corresponding migration both need updating.
EMBEDDING_DIM = 384


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True)
    # OpenAlex's work ID — our idempotency key for ingestion upserts.
    openalex_work_id = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    abstract = Column(Text, nullable=True)  # nullable: some OpenAlex works lack an abstract
    year = Column(Integer, nullable=True, index=True)

    # Populated during ingestion (Phase 5) from the abstract via sentence-transformers.
    # Nullable so ingestion can insert paper rows before embeddings are generated.
    embedding = Column(Vector(EMBEDDING_DIM), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    authors = relationship("PaperAuthor", back_populates="paper", cascade="all, delete-orphan")
    topics = relationship("PaperTopic", back_populates="paper", cascade="all, delete-orphan")

    # Full-text search on title + abstract is done via a functional GIN index created
    # directly in the migration (see alembic/versions/), not a stored tsvector column here
    # — keeps the model simple and the index in sync automatically with no trigger needed.
