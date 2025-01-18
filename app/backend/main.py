from fastapi import FastAPI
from app.backend.routes import user, auth, auction, bid, categories
from fastapi.middleware.cors import CORSMiddleware
from app.backend.routes.bid import aukcii
from app.backend.database import get_db
import asyncio

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


async def periodic_task():
    while True:
        db = next(get_db())
        await aukcii(db=db)
        await asyncio.sleep(10)


@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(periodic_task())


@app.get("/")
async def root():
    return {"message": "Hello World"}


