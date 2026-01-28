from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class AuctionResponse(BaseModel):
    auction_id: int
    title: str
    starting_price: float
    is_active: bool
    start_time: Optional[datetime]
    end_time: Optional[datetime]

class BidResponse(BaseModel):
    bid_id: int
    amount: float
    user_id: int
    auction_id: int

class UserResponse(BaseModel):
    id: int
    username: str

class LogInResponse(BaseModel):

