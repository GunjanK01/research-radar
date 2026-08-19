from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    # Our own topic label (e.g. "Large Language Models", "Computer Vision") assigned
    # during ingestion based on which OpenAlex search query surfaced the paper — not
    # a direct mirror of OpenAlex's own concept taxonomy. See DECISIONS_LOG.
    name = Column(String, unique=True, nullable=False, index=True)

    papers = relationship("PaperTopic", back_populates="topic")
