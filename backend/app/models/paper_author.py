from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class PaperAuthor(Base):
    """
    Explicit association object (not a bare Table) because we need an extra column:
    author_position, so the detail page can display authors in the correct order
    rather than an arbitrary one.
    """
    __tablename__ = "paper_authors"

    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True)
    author_position = Column(Integer, nullable=False)  # 0-indexed order of appearance

    paper = relationship("Paper", back_populates="authors")
    author = relationship("Author", back_populates="papers")
