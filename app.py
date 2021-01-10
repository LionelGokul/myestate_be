from flask import Flask
from flask_cors import CORS
from models import db

# initializing APP
app = Flask("MyEstate", static_url_path='/static', static_folder='static')

# Configuring Connection String
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kpn9zmuqp42zsn62:uqs0ytg455a2pz40@j21q532mu148i8ms.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/mh3o48ev1avf0yed'
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
