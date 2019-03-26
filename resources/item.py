from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    # ensure price argument is present
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be left blank."
    )

    parser.add_argument("store_id",
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    #extracted into separate find_by_name class method so a JWT token isn't required for internal calls
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found."}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name {} exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {"message":"An error occured inserting the item."}, 500 #internal server error

        return item.json(), 201 #created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted."}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]} # .all() == return all objects in the database; list comprehension to structure
