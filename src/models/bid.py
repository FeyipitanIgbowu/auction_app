class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    auction_id = db.Column(db.Integer, db.ForeignKey("auction.id"))
