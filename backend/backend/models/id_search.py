from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.db.base import Base

class IDSearch(Base):
    __tablename__ = "id_searches"

    id = Column(Integer, primary_key=True, index=True)
    id_number = Column(String, unique=True, index=True)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String, nullable=False)
    citizen = Column(Boolean, nullable=False)
    search_count = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with holidays
    holidays = relationship("Holiday", back_populates="id_search", cascade="all, delete-orphan")

class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    id_search_id = Column(Integer, ForeignKey("id_searches.id"))
    name = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime, nullable=False)
    type = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship with id_search
    id_search = relationship("IDSearch", back_populates="holidays")
