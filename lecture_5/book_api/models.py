from typing import Optional

from sqlalchemy import Column, Integer, String

from database import Base


class Book(Base):
    __tablename__ = "books"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, nullable=False, index=True)  
    author: str = Column(String, nullable=False, index=True)  
    year: Optional[int] = Column(Integer, nullable=True, index=True) 
