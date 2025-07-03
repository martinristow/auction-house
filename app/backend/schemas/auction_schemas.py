from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Auction(BaseModel):
    id: int
    title: str
    description: str
    starting_price: float
    img: str
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CreateAuction(BaseModel):
    title: str
    description: str
    starting_price: float
    img: str
    end_date: Optional[datetime] = None


class UpdateAuction(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    starting_price: Optional[float] = None
    img: Optional[str] = None
    end_date: Optional[datetime] = None
