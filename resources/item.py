import uuid
from json import loads

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items

blp = Blueprint("Items", __name__, description='Operations on items')


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get_item(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")

    def delete_item(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")

    def put(self, item_id):
        item_data = loads(request.data.decode('utf-8'))
        if "price" not in item_data or "name" not in item_data:
            abort(400, message="Bad request. Ensure price, name are included in data")
        try:
            item = items[item_id]
            item |= item_data

        except KeyError:
            abort(404, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = loads(request.data.decode('utf-8'))
        if ("price" not in item_data or
                "store_id" not in item_data or
                "name" not in item_data):
            abort(400, message="Bad request")
        for item in items.values():
            if item_data["name"] == item['name'] and item_data['store_id'] == item['store_id']:
                abort(400, message="Item already exist")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201
