auction_blue_print = Blueprint("auction", __name__)

def get_db_session():
    return db.session

@auction_blue_print.route("/", methods=["POST"])
def create_auction():
    data = request.get_json()
    title = data.get("title")
    starting_price = data.get("starting_price")

    service = AuctionService(get_db_session())
    auction = service.create_auction(title, starting_price)

    return jsonify({
        "auction_id": auction.id,
        "title" : auction.title,
        "starting_price" : auction.starting_price,
        "is_active": auction.is_active,
        "starting_time": auction.starting_time.isoformat(),
    })

@auction_blue_print.route("/auctions/<int:auction_id>/bids", methods=["POST"])
def place_bid(auction_id):
    data = request.get_json()
    user_id = data.get("user_id")
    amount = data.get("amount")

    db = get_db_session()
    user = db.query(User).get(user_id)
    service = AuctionService(db, auction_id)

    try:
        bid = service.place_bid(amount, user)
    except ValueError as e:
        return jsonify({"Error..": str(e)}),

    return jsonify({
        "bid_id": bid.id,
        "amount": bid.amount,
        "user_id": bid.user_id,
        "auction_id": bid.auction_id,
    })

@auction_blue_print.route("/auctions/<int:auction_id>", methods=["GET"])
def get_auction_details(auction_id):
    service = AuctionService(get_db_session(), auction_id)
    try:
        auction_details = service.get_auction_details()
    except ValueError as e:
        return jsonify({"Error..": str(e)}),

    return jsonify({auction_details})