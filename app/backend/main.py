from fastapi import FastAPI
# from app import models
# from .database import engine
from app.backend.routes import user, auth, auction, bid, categories
from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.create_all(bind=engine)



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Дозволи пристап од сите домени
    allow_credentials=True,
    allow_methods=["*"],  # Дозволи сите HTTP методи
    allow_headers=["*"],  # Дозволи сите HTTP хедери
)


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(auction.router)

app.include_router(bid.router)

app.include_router(categories.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}