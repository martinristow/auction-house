from fastapi import FastAPI
# from app import models
# from .database import engine
from app.backend.routes import user, auth

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}