from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class PaperTopic(Base):
    __tablename__ = "paper_topics"

    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True)

    paper = relationship("Paper", back_populates="topics")
    topic = relationship("Topic", back_populates="papers")
