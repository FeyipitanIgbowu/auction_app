from tkinter.font import names

import pytest
from flask import Flask
from src.routes.routes import auction_blueprint
from src.database.database import db
from src.models.auction import Auction
from src.models.user import User
from src.models.bid import Bid
from datetime import datetime

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(auction_blueprint)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session


def test_that_auction_can_be_created(client, session):
    response = client.post("/auctions/", json={
        "title":"Himalaya_birkin",
        "starting_price": 100
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Himalaya_birkin"
    assert data["starting_price"] == 100
    assert data["is_active"] is True


def test_that_auction_details_can_be_gotten(client, session):
    auction = Auction(
        title="Bag Auction",
        starting_price=200,
        is_active=True,
        start_time=datetime.now(),
        end_time=datetime.now(),
    )
    session.add(auction)
    session.commit()

    response = client.get(f"/auctions/{auction.id}")
    assert response.status_code == 201 or response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Bag Auction"
    assert data["starting_price"] == 200
    assert data["is_active"] is True


def test_that_you_can_place_bid_successfully(client, session):
    user = User(
        username = "Chiamie",
        password = "nutrient"
    )
    auction = Auction(
        title = "Bag Auction",
        starting_price = 200,
        is_active = True,
        start_time = datetime.now(),
        end_time = datetime.now(),
    )
    session.add_all([user, auction])
    session.commit()

    response = client.post(f"/auctions/{auction.id}/bids", json={
        "user_id": user.id,
        "amount": 250,
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["amount"] == 250
    assert data["user_id"] == user.id
    assert data["auction_id"] == auction.id


def test_that_you_cannot_bid_lower_amount_than_the_first_bid(client, session):
    user = User(
        username = "Chiamie",
        password = "nutrient"
    )
    auction = Auction(
        title = "Bag Auction",
        starting_price = 200,
        is_active = True,
        start_time = datetime.now(),
        end_time = datetime.now(),
    )
    session.add_all([user, auction])
    session.commit()
    response1 = client.post(f"/auctions/{auction.id}/bids", json={
        "user_id": user.id,
        "amount": 250,
    })
    response2 = client.post(f"/auctions/{auction.id}/bids", json={
        "user_id": user.id,
        "amount": 150,
    })
    assert response1.status_code == 201
    assert response2.status_code == 400
    data = response2.get_json()
    assert "Bid must be higher than current bid" in data["error"]


def test_that_you_cannot_place_bid_on_closed_auction(client, session):
    user = User(
        username = "Chiamie",
        password = "nutrient"
    )
    auction = Auction(
        title = "Bag Auction",
        starting_price = 200,
        is_active = False,
    )
    session.add_all([user, auction])
    session.commit()

    response =  client.post(f"/auctions/{auction.id}/bids", json={
        "user_id": user.id,
        "amount": 250,
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "Auction is closed" in data["error"]

def test_that_you_cannot_access_a_nonexistent_auction(client, session):
    response = client.get("/auctions/999")
    assert response.status_code == 404
    data = response.get_json()
    assert "Auction does not exist" in data["error"]


