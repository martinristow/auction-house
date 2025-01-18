from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from app.backend import models
from ..schemas import bids_schemas
from typing import List
from ..oauth2 import get_current_user
from datetime import datetime, timezone
from app.backend.send_email import email_send
from sqlalchemy.orm import aliased
router = APIRouter(tags=["Bids"])


@router.get("/bids/{id}", response_model=List[bids_schemas.BidOut])
async def get_bids(id: int, db: Session = Depends(get_db)):

    bids = db.query(models.Bids).filter(id == models.Bids.auction_id).all()
    if bids is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="At this moment we have not any bids!")

    return bids



@router.post("/bids", status_code=status.HTTP_201_CREATED, response_model=bids_schemas.CreateBids)
async def create_bids(bid_data: bids_schemas.CreateBids, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    # Proveri dali aukcijata postoi
    id: int = bid_data.auction_id
    auction = db.query(models.Auction).filter(id == models.Auction.id).first()
    if auction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auction with id {id} does not exist."
        )

    # proverka dali aukcijata e aktivna
    if not auction.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This auction is no longer active.")


    # ja zemame sumata na bidderot sto ja vnel
    bidder_price = bid_data.amount

    # proverka dali vnesenata suma e pogolema od 0 -> ne dozvoluvame negativni broevi
    if bidder_price <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The Number must be greater than 0!")


    # dali postoe nekakva aukcija vo bids - > ja gledame poslednata dodadena vrednost vo tabelata
    bids = db.query(models.Bids).filter(id == models.Bids.auction_id).order_by(models.Bids.id.desc()).first()
    if bids is None:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nema takva aukcija vo Bids")

        # ja zimame vrednosta starting price od tabelata auction
        auction_starting_price = auction.starting_price

        # sumata od auction tabelata ja zgolemuvame za 10 procenti
        price_ten_percent = (auction_starting_price * 0.10) + auction_starting_price


        # pravime proverka ako bidderot vnese pomala suma od 10 posto od prethodnata
        if bidder_price < price_ten_percent:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Your bid must be at least {price_ten_percent:.2f}. Current bid is too low.")

        # gi zimame podatocite i kreirame bids
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



async def aukcii(db: Session):
    current_time = datetime.now(timezone.utc)  # momentalnoto vreme

    auctions = db.query(models.Auction).all()  # site aukcii
    for auction in auctions:

        end_date = auction.end_date

        # proverka dali momentalnoto vreme e pogolemo od end_date na aukcijata
        if current_time > end_date:
            auction.is_active = False  # ja zatvarame aukcijata dokolku vremeto e pominato
            auction.end_date = "2090-01-16 18:13:22.292194+01"  # ova e test vrednost koja vo sledniot update ke bide promeneta na podobar nacin

            # Alias za ponudata -> privremeno ime za tabelata za povrzuvanje na tabeli bez da imame konflikti
            bid_alias = aliased(models.Bids)

            # posledniot ponuduvac go vadime
            last_bidder = (
                db.query(models.User)
                .join(bid_alias, bid_alias.bidder_id == models.User.id)
                .filter(bid_alias.auction_id == auction.id)
                .order_by(bid_alias.id.desc())
                .first()
            )

            user_email = last_bidder.email

            print(user_email)

            db.commit()
            db.refresh(auction)

            # povik na email_send funkcija -> logikata ja delam za pogolema citlivost
            await email_send(auction.title, user_email=user_email)

            # return user_email