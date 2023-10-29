import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from models import Todo, TodoModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from decouple import config
import models
import database




app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    pool = redis.ConnectionPool.from_url(config('REDIS_URL'))
    redis_client = redis.StrictRedis(connection_pool=pool)
    await FastAPILimiter.init(redis_client)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def root():
    return {"message": "Hello World"}  


@app.get("/todos", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()


@app.get("/todos/{todo_id}", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_dict = {
        "id": todo.id,
        "item": todo.item
    }
    return JSONResponse(content=todo_dict, status_code=200)



@app.post("/todos", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
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

@app.delete("/todos/{todo_id}", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def delete_todos(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "deleted"}



