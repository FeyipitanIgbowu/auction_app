from flask import Blueprint, render_template, request, jsonify
from src.services.auction_service import AuctionService
from src.database.database import db
from src.models.auction import Auction
from src.models.user import User
from src.dto.response.auction_responses import AuctionResponse, BidResponse, UserResponse

auction_blueprint = Blueprint('auction', __name__, url_prefix='/auctions')

def get_db_session():
    return db.session

@auction_blueprint.route("/", methods=["POST"])
def create_auction():
    data = request.get_json()
    title = data.get("title")
    starting_price = data.get("starting_price")

    service = AuctionService(get_db_session())
    auction = service.create_auction(title, starting_price)

    response = AuctionResponse(
        auction_id = auction.id,
        title = auction.title,
        starting_price = auction.starting_price,
        is_active = auction.is_active,
        start_time = auction.start_time,
        end_time = auction.end_time
    )
    return jsonify(response.dict()), 201

@auction_blueprint.route("/<int:auction_id>/bids", methods=["POST"])
def place_bid(auction_id):
    data = request.get_json()
    user_id = data.get("user_id")
    amount = data.get("amount")

    db = get_db_session()
    user = db.get(User, user_id)
    service = AuctionService(db, auction_id)

    try:
        bid = service.place_bid(amount, user)
        response = BidResponse(
            bid_id = bid.id,
            amount = bid.amount,
            user_id = bid.user_id,
            auction_id = bid.auction_id
        )
        return jsonify(response.dict()), 201
    except ValueError as e:
        return {"error": str(e)}, 400


@auction_blueprint.route("/<int:auction_id>", methods=["GET"])
def get_auction_details(auction_id):
    service = AuctionService(get_db_session(), auction_id)
    try:
        auction_details = service.get_auction_details()
        return jsonify(auction_details), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

