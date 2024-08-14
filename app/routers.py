from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, crud

router = APIRouter()

models.Base.metadata.create_all(engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    templates = Jinja2Templates(directory="./app/templates")
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/task")
async def get_tasks(db: Session = Depends(get_db)):
	tasks = await crud.get_all_tasks(db=db)
	return tasks

@router.post("/task")
async def create_task(title: str, db: Session = Depends(get_db)):
	task = await crud.create_task(db=db, title=title)
	return task

@router.put("/task/{task_id}")
async def toggle_task(task_id: int, db: Session = Depends(get_db)):
	task = await crud.toggle_task(db=db, task_id=task_id)
	return task

@router.delete("/task/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
	task = await crud.delete_task(db=db, task_id=task_id)
	return task