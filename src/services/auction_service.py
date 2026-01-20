from src.models.auction import Auction
from src.models.user import User
from src.models.bid import Bid
from datetime import datetime
from src.database.database import db
import sched, time
import threading


class AuctionService:
    def __init__(self, db_session, auction_id=None):
        self.db = db_session
        self.auction_id = auction_id
        self.scheduler = sched.scheduler(time.time, time.sleep)


    def create_auction(self, title, starting_price):
        auction = Auction(
            title=title,
            starting_price=starting_price,
            is_active=True,
            start_time=datetime.now(),
        )
        self.db.add(auction)
        self.db.commit()
        self.auction_id = auction.id

        self.scheduler.enter(600, 1, self.end_auction, argument=(auction.id))
        threading.Thread(target=self.scheduler.run, daemon=True).start()
        return auction

    def place_bid(self, amount, user):
        auction = self.db.get(Auction, self.auction_id)
        if not auction:
            raise ValueError("Auction does not exist")
        if not auction.is_active:
            raise ValueError("Auction is closed")

        highest_bid_amount = auction.get_highest_bid()
        if amount <= highest_bid_amount:
            raise ValueError("Bid must be higher than current bid")

        bid = Bid(amount=amount, user=user, auction_id=self.auction_id)
        self.db.add(bid)
        self.db.commit()
        return bid

    def get_auction_details(self):
        auction = self.db.get(Auction, self.auction_id)
        if not auction:
            raise ValueError("Auction does not exist")

        return {
            "id": auction.id,
            "title": auction.title,
            "starting_price": auction.starting_price,
            "is_active": auction.is_active,
            "highest_bid": auction.get_highest_bid()
        }

    def get_highest_bidder(self):
        auction = self.db.get(Auction, self.auction_id)
        if not auction or not auction.bids:
            return None
        return auction.get_highest_bid()

