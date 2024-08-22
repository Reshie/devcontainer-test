from typing import List
from elasticsearch import Elasticsearch
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, crud
from app.schemas import Task, TaskCreate

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

@router.get("/task", response_model=List[Task])
def get_tasks(db: Session = Depends(get_db)):
	tasks = crud.get_all_tasks(db=db)
	return tasks

@router.post("/task", response_model=Task)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
	task = crud.create_task(db=db, title=data.title)
	return task

@router.put("/task/{task_id}", response_model=Task)
def toggle_task(task_id: int, db: Session = Depends(get_db)):
	task = crud.toggle_task(db=db, task_id=task_id)
	return task

@router.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
	task = crud.delete_task(db=db, task_id=task_id)
	return task

@router.get("/search", response_class=HTMLResponse)
async def root(request: Request):
    templates = Jinja2Templates(directory="./app/templates")
    return templates.TemplateResponse("search.html", {"request": request})

@router.post("/search")
def search_es(q: str):
	query = {
		"query": {
			"bool": {
				"should": [
					{"match": {"title": q}},
					{"match": {"author": q}}
				]
			}
		}
	}
	es = Elasticsearch("http://elasticsearch:9200")
	res = es.search(index="literature", body=query)
	es.close()
	return res['hits']['hits']