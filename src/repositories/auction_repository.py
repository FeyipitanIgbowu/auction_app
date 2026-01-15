class AuctionRepository:

    def save(self, auction):
        db.session.add(auction)
        db.session.commit()
        return auction

    def find_by_id(self, id):
        return Auction.query.get(id)

    def delete(self, auction):
        db.session.delete(auction)
        db.session.commit()

    def update(self, auction):
        db.session.commit()
