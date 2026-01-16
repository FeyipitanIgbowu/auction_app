from pydantic import BaseModel

class AuctionRequest(BaseModel):
    title: str
    starting_price: float

class BidRequest(BaseModel):
    user_id: int
    amount: float

class UserRequest(BaseModel):
    username: str
    password: str