from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未命名')
    binding = Column(String(30))
    publisher = Column(String(50))
    price = Column(String(30))
    pages = Column(Integer)
    pubdate = Column(String(30))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))  #简介
    image = Column(String(50))
