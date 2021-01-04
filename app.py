from flask import Flask
from flask_cors import CORS
from models import db

# initializing APP
app = Flask("MyEstate", static_url_path='/static', static_folder='static')

# Configuring Connection String
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hhwkd7s7t69nfydq:y2wojvhvzu1f3e3z@l0ebsc9jituxzmts.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/uvx1dgkqm0ohu0hm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['aws_access_key_id'] = 'AKIAI65DIV5RWERXPVLA'
app.config['aws_secret_access_key'] = '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'


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
