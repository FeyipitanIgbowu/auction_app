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

class LogInRequest(BaseModel):
    username: str
    password: str

class SignUpRequest(BaseModel):
    name: str
    email: str
    phone_number: str
    address: str
    username: str
    password: str