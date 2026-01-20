from flask import Flask
from config import Config
from src.database.database import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

from src.routes.routes import auction_blueprint
app.register_blueprint(auction_blueprint)