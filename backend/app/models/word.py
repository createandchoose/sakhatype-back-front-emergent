from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Word(Base):
    """Word model for typing tests."""
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String, nullable=False, index=True)
