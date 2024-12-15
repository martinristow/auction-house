from fastapi import FastAPI
# from app import models
# from .database import engine
from app.routes import user

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}