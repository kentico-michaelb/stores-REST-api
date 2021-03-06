import os

from flask import Flask
from flask_restful import Api, reqparse  # remember: run activate.bat for venv installation
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db") # os.environ.get(for HeroKu, fallback local var)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #turn off Flask's modification tracker and use primary SQLAlchemy's
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth created

api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>") #http://127.0.0.1"5080/student/<name>
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")

#prevent app.run from running if app is imported
#__main__ is a python assigned name if the app is run directly
if __name__=="__main__":
    from db import db #may not work due to project structure
    db.init_app(app)
    app.run(port=5080, debug=True)
