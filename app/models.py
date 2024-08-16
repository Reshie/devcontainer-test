from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from app.database import Base

class Task(Base):
	__tablename__ = 'tasks'
		
	id = Column(Integer, primary_key=True, autoincrement= True)
	title = Column(String)
	is_done = Column(Boolean, default=False)