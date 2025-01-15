from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateAuction(BaseModel):
    title: str
    description: str
    starting_price: float
    end_date: datetime | None = None


class AuctionOut(CreateAuction):
    id: int
    created_at: datetime
    owner_id: int


class UpdateAuction(BaseModel):
    title: str
    description: str
    starting_price: float
