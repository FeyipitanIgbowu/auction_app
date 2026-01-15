class BidRepository:
    def __init__(self):
        pass

    def save_bid(self, bid):
        bid = Bid(bid)
        bid.save()
