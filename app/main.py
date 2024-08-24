from fastapi import FastAPI
from controllers import users, posts

from db import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(users.router, prefix="/api")
app.include_router(posts.router, prefix="/api")


@app.get("/")
def home():
    return {"message": "First FastAPI app"}
