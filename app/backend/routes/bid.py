from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from app.backend import models
from ..schemas import bids_schemas
from typing import List


router = APIRouter(tags=["Bids"])


@router.get("/bids/{id}", response_model=List[bids_schemas.BidOut])
async def get_bids(id: int, db: Session = Depends(get_db)):

    bids = db.query(models.Bids).filter(id == models.Bids.auction_id).all()
    if bids is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="At this moment we have not any bids!")

    return bids



@router.post("/bids", response_model=bids_schemas.CreateBids)
async def create_bids():
    pass