from app import app
from db import db

db.init_app(app)

#leverage SQLAlchemy to create tables before first request
@app.before_first_request
def create_tables():
    db.create_all() # creates tables based upon the imported classes/resources. e.g. from resources.store import Store, StoreList
