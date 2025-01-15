from pydantic import BaseModel


class CreateBids(BaseModel):
    amount: float
    auction_id: int
    bidder_id: int



class BidOut(CreateBids):
    id: int