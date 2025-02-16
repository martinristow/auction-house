from fastapi import status, Depends, HTTPException, APIRouter
from ..schemas import auction_schemas
from ..database import get_db
from app.backend import models
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from typing import List
from sqlalchemy.orm import aliased
router = APIRouter(tags=["Auctions"])


@router.post("/auctions", status_code=status.HTTP_201_CREATED, response_model=auction_schemas.AuctionOut)
async def create_auction(auction_data: auction_schemas.CreateAuction, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    is_admin = db.query(models.User).filter(models.User.id == current_user.id, models.User.is_admin == True).first()

    if is_admin:

        new_auction = models.Auction(**auction_data.dict())
        new_auction.owner_id = current_user.id

        db.add(new_auction)
        db.commit()
        db.refresh(new_auction)

        return new_auction

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be admin to create auction")





@router.get("/auctions-all", status_code=status.HTTP_200_OK, response_model=List[auction_schemas.AuctionOut])
async def all_auctions(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    auctions = db.query(models.Auction).all()

    return auctions


@router.get("/auctions/{id}", status_code=status.HTTP_200_OK, response_model=auction_schemas.AuctionOut)
async def get_auction(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # auction = db.query(models.Auction).filter(id == models.Auction.id).first()
    user_aliased = aliased(models.User)
    auction = db.query(models.Auction).join(user_aliased,
                                            user_aliased.id == models.Auction.owner_id).filter(id == models.Auction.id).first()

    if auction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Auction with id: {id} is not exist")

    return auction



@router.delete("/auctions/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_auction(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    auction = db.query(models.Auction).filter(id == models.Auction.id, current_user.id == models.Auction.owner_id).first()

    if auction:
        db.delete(auction)
        db.commit()

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Auction not found or you're not the owner!")



@router.patch("/auctions/{id}", status_code=status.HTTP_200_OK, response_model=auction_schemas.AuctionOut)
async def update_auction(id: int, update_data: auction_schemas.UpdateAuction, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    auction_query = db.query(models.Auction).filter(id == models.Auction.id, models.Auction.owner_id == models.User.id)

    auction = auction_query.first()

    if auction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Auction not found or you're not the owner!")



    auction_query.update(update_data.model_dump(), synchronize_session=False)
    db.commit()

    return auction_query.first()