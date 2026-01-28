from flask import Flask
from config import Config
from src.database.database import db
from src.routes.routes import auction_blueprint


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.config["JWT_SECRET_KEY"] = 'super secret key'
jwt = JWT(app)
app.register_blueprint(auction_blueprint)