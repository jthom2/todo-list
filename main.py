from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from models import Todo, TodoModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import database




app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}  


@app.get("/todos")
async def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()


@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_dict = {
        "id": todo.id,
        "item": todo.item
    }
    return JSONResponse(content=todo_dict, status_code=200)



@app.post("/todos")
async def create_todo(item: str, db: Session = Depends(get_db)):
    todo = TodoModel(item=item)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.put("/todos/{todo_id}")
async def update_todos(todo_id: int, item: str, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.item = item
    db.commit()
    db.refresh(todo)
    todo_dict = {
        "id": todo.id,
        "item": todo.item
    }
    return todo_dict

@app.delete("/todos/{todo_id}")
async def delete_todos(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "deleted"}


