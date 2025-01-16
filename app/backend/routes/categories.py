from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from app.backend import models
from ..schemas import auction_schemas
from typing import List


router = APIRouter(tags=["Categories"])


@router.get("/categories/active-auctions", response_model=List[auction_schemas.AuctionOut])
async def get_all_active_auctions(db: Session = Depends(get_db)):

    active_auctions = db.query(models.Auction).filter("true" == models.Auction.is_active).order_by(models.Auction.id.desc()).all()

    if active_auctions is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This moment we do not have any auctions!")

    return active_auctions


@router.get("/categories/closed-auctions", response_model=List[auction_schemas.AuctionOut])
async def get_all_closed_auctions(db: Session = Depends(get_db)):

    closed_auctions = db.query(models.Auction).filter("false" == models.Auction.is_active).order_by(models.Auction.id.desc()).all()

    if closed_auctions is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This moment we do not have any auctions!")

    return closed_auctions



@router.get("/categories/all", response_model=List[auction_schemas.AuctionOut])
async def get_all_categories(db: Session = Depends(get_db)):

    all_auctions = db.query(models.Auction).order_by(models.Auction.id.desc()).all()

    if all_auctions is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This moment we do not have any auctions!")

    return all_auctions