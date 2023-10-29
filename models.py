from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

class TodoModel(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String)

class Todo(BaseModel):
    id: int
    item: str