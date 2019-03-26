from db import db

class StoreModel(db.Model):
    #SQLAlchemy table definition
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # items is a List due to 1:M relationship of store:items
    items = db.relationship("ItemModel", lazy="dynamic") # lazy == avoid creating a lot of entries all at once at StoreModel creation

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name": self.name, "items": [item.json() for item in self.items.all()]} # .all is querybuilder method to offset lazy

    @classmethod
    def find_by_name(cls, name): #cls == ItemModel
        return cls.query.filter_by(name=name).first() #SQLAlchemy query builder == SELECT * FROM items WHERE name=name

    def save_to_db(self):
        db.session.add(self) #you can add multiple objects in a single session
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self) #you can add multiple objects in a single session
        db.session.commit()
