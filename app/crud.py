from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models

def get_all_tasks(db: Session):
    return db.query(models.Task).all()

def get_task(db: Session, task_id: int):
	db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
	if db_task is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return db_task

def create_task(db: Session, title: str):
	db_task = models.Task(title=title)
	try:
		db.add(db_task)
	except:
		raise HTTPException(status_code=500, detail="error")  
	db.commit()
	db.refresh(db_task)
	return db_task

def toggle_task(db: Session, task_id: int):
	db_task = get_task(db, task_id)
	db_task.is_done = not db_task.is_done
	db.commit()
	db.refresh(db_task)
	return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    db.delete(db_task)
    db.commit()
    return db_task