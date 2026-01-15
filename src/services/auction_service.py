class AuctionService:
    def __init__(self, db_session, auction_id=None):
        self.db = db_session
        self.auction_id = auction_id

    def create_auction(self, title, starting_price):
        auction = Auction(
            title=title,
            starting_price=starting_price,
            is_active=True,
            starting_time=datetime.now(),
        )
        self.db.add(auction)
        self.db.commit()
        self.auction_id = auction.id
        return auction

    def place_bid(self, user, amount):
        auction = Auction.query.get(self.auction_id)
        if not auction:
            raise ValueError("Auction does not exist")
        if not auction.is_active:
            raise ValueError("Auction is closed")
        if amount <= auction.get_highest_bid():
            raise ValueError("Bid must be higher than current highest bid")

        bid = Bid(amount=amount, user=user, auction=auction)
        self.db.add(bid)
        self.db.commit()
        return bid

    def get_auction_details(self):
        auction = Auction.query.get(self.auction_id)
        if not auction:
            raise ValueError("Auction does not exist")

        return {
            "id": auction.id,
            "title": auction.title,
            "starting_price": auction.starting_price,
            "is_active": auction.is_active,
            "highest_bid": auction.get_highest_bid()
        }
