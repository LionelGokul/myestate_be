from flask import Flask
from flask_cors import CORS
from models import db

# initializing APP
app = Flask("MyEstate", static_url_path='/static', static_folder='static')

# Configuring Connection String
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cs6lt3l6dc3g62o6:wsjgr00mmdqsno43@l0ebsc9jituxzmts.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/n7cu9urc46v84xao'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

# Cross Origin Resource Sharing
CORS(app, resources={r"/*": {"origins": "*"}})

# initializing db
db.init_app(app)
with app.app_context():
    db.create_all()

from urls import configure_URL

# initializing Routes
configure_URL(app)

if __name__ == "__main__":
    app.run(debug=True)
