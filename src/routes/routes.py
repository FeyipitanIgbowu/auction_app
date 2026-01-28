from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt
)
from werkzeug.security import check_password_hash

from src.services.auction_service import AuctionService
from src.database.database import db
from src.models.user import User
from src.dto.response.auction_responses import AuctionResponse, BidResponse

auction_blueprint = Blueprint("auction", __name__, url_prefix="/auctions")


def get_db_session():
    return db.session


@auction_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    session = get_db_session()
    user = session.query(User).filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role}
    )

    return jsonify(access_token=access_token), 200


@auction_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_auction():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    data = request.get_json()
    title = data.get("title")
    starting_price = data.get("starting_price")

    service = AuctionService(get_db_session())
    auction = service.create_auction(title, starting_price)

    response = AuctionResponse(
        auction_id=auction.id,
        title=auction.title,
        starting_price=auction.starting_price,
        is_active=auction.is_active,
        start_time=auction.start_time,
        end_time=auction.end_time
    )

    return jsonify(response.dict()), 201


@auction_blueprint.route("/<int:auction_id>/bids", methods=["POST"])
@jwt_required()
def place_bid(auction_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    amount = data.get("amount")

    session = get_db_session()
    user = session.get(User, user_id)

    service = AuctionService(session, auction_id)

    try:
        bid = service.place_bid(amount, user)
        response = BidResponse(
            bid_id=bid.id,
            amount=bid.amount,
            user_id=bid.user_id,
            auction_id=bid.auction_id
        )
        return jsonify(response.dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auction_blueprint.route("/<int:auction_id>", methods=["GET"])
def get_auction_details(auction_id):
    service = AuctionService(get_db_session(), auction_id)
    try:
        auction_details = service.get_auction_details()
        return jsonify(auction_details), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
