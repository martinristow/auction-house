from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from app.backend import models
from ..schemas import bids_schemas
from typing import List
from ..oauth2 import get_current_user
router = APIRouter(tags=["Bids"])


@router.get("/bids/{id}", response_model=List[bids_schemas.BidOut])
async def get_bids(id: int, db: Session = Depends(get_db)):

    bids = db.query(models.Bids).filter(id == models.Bids.auction_id).all()
    if bids is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="At this moment we have not any bids!")

    return bids



@router.get("/bids", status_code=status.HTTP_201_CREATED, response_model=bids_schemas.CreateBids)
async def create_bids(bid_data: bids_schemas.CreateBids, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):


    # Proveri dali aukcijata postoi
    id: int = bid_data.auction_id
    auction = db.query(models.Auction).filter(id == models.Auction.id).first()
    if auction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auction with id {id} does not exist."
        )

    # dali postoe nekakva aukcija vo bids - > ja gledame poslednata dodadena vrednost vo tabelata
    bids = db.query(models.Bids).filter(id == models.Bids.auction_id).order_by(models.Bids.id.desc()).first()
    if bids is None:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nema takva aukcija vo Bids")

        # ja zimame vrednosta starting price od tabelata auction
        auction_starting_price = auction.starting_price

        # sumata od auction tabelata ja zgolemuvame za 10 procenti
        price_ten_percent = (auction_starting_price * 0.10) + auction_starting_price

        # ja zemame sumata na bidderot sto ja vnel
        bidder_price = bid_data.amount

        # pravime proverka ako bidderot vnese pomala suma od 10 posto od prethodnata
        if bidder_price < price_ten_percent:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Your bid must be at least {price_ten_percent:.2f}. Current bid is too low.")

        # gi zimame podatocite i kreirame bid
        new_bid = models.Bids(**bid_data.model_dump())
        new_bid.bidder_id = current_user.id

        db.add(new_bid)
        db.commit()
        db.refresh(new_bid)

        return new_bid


    # Dokolku postoi aukcija vo bids znaci ja zemame negovata vrednost od amount i pravime proverka na sumata za 10% pogolema od starata

    # ja zemame prvata vrednost za iznosot od bids tabelata
    bid_amount = bids.amount

    # cenata ja zgolemuvame za 10 procenti
    price_ten_percent = (bid_amount * 0.10) + bid_amount

    # ja zemame ponudata sto bidderot ja ponuduva
    bidder_price = bid_data.amount

    # pravime proverka dali sumata na bidderot e pomala od sumata od 10 posto
    if bidder_price < price_ten_percent:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Your bid must be at least {price_ten_percent:.2f}. Current bid is too low.")

    # Dokolku se e vo red gi zimame podatocite i gi zapisuvame vo bazata
    new_bid = models.Bids(**bid_data.model_dump())
    new_bid.bidder_id = current_user.id

    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)

    return new_bid
