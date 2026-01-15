class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    starting_price = db.Column(db.Float)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    bids = db.relationship("Bid", backref="auction", lazy=True)

    def get_highest_bid(self):
        if not self.bids:
            return self.starting_price
        highest_bid = max(self.bids, key=lambda b: b.amount)
        return highest_bid.amount, highest_bid.created_at

    # def close_auction(self):
    #     self.is_active = False

    def active_bid(self):
        return self.is_active

    def can_accept_bid(self, amount):
        return self.is_active and amount > self.get_highest_bid()
