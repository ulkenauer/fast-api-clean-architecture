from sqlalchemy import Column, String, Integer, DateTime, func

from src.base import Base


class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String(100), index=True, nullable=False)
    text = Column(String(1024), index=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
