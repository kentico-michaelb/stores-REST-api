from db import db

class ItemModel(db.Model):
    #SQLAlchemy table definition
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))#number after decimal point

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name): #cls == ItemModel
        return cls.query.filter_by(name=name).first() #SQLAlchemy query builder == SELECT * FROM items WHERE name=name

    def save_to_db(self):
        db.session.add(self) #you can add multiple objects in a single session
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self) #you can add multiple objects in a single session
        db.session.commit()
