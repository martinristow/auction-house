from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateAuction(BaseModel):
    title: str
    description: str
    starting_price: float
    end_date: datetime | None = None



class UserOut(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True



class AuctionOut(CreateAuction):
    id: int
    created_at: datetime
    owner_id: int
    is_active: bool
    owner: UserOut

    class Config:
        from_attributes = True



class UpdateAuction(BaseModel):
    title: str
    description: str
    starting_price: float
