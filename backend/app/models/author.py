from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    # OpenAlex's own author ID, used as the natural key for idempotent upserts during
    # ingestion (an author can appear on many papers; we don't want duplicate rows).
    openalex_author_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)

    papers = relationship("PaperAuthor", back_populates="author")
