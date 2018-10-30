from flask import request, jsonify, make_response
from flask_restplus import Resource
from pymongo import MongoClient

from ..util.dto import InventoryDto

MdbURI = 'mongodb://user0:countries9@ds145463.mlab.com:45463/sayuni_db'
client = MongoClient(MdbURI)
db = client['sayuni_db']

coll = db.inventory


api = InventoryDto.api
_product = InventoryDto.product


@api.route('/')
class Inventory(Resource):

    @api.doc('List_of_Inventory_products')
    @api.marshal_list_with(_product, envelope='data')
    def get(self):
        """List all products"""
        product_list = []
        for product in coll.find():
            product_list.append({
                "name": product['name'],
                "quantity": product['quantity'],
                "price": product['price']
            })
        return product_list

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_product, validate=True)
    def post(self):
        """Creates a new Product """
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            existing_product = data.get("name")
            if existing_product:
                if coll.find_one({'name': data.get("name")}):
                    return {"response": "Product already exists"}
                else:
                    coll.insert(data)
                    return make_response(
                        "{name} successfully created".format(
                            name=data.get("name")), 201
                    )
            else:
                return {"response": "Product name missing"}


@api.route('/<name>')
@api.param('name', 'The Product name')
@api.response(404, 'Product not found.')
class Product(Resource):

    @api.doc('get a product')
    @api.marshal_with(_product)
    def get(self, name):
        """get a product given its name"""
        existing_product = coll.find_one({'name': name})
        if existing_product:
            return existing_product
        else:
            api.abort(404)

    @api.doc('Delete a product')
    def delete(self, name):
        """Delete a product given its name"""
        existing_product = coll.find_one({'name': name})
        if existing_product:
            coll.remove(existing_product)
            return make_response(
                "{name} successfully deleted".format(name=name), 201
            )
        else:
            return make_response(
                "{name} not found".format(name=name)
            )

    @api.doc('Change a products detailes')
    @api.expect(_product, validate=True)
    def put(self, name):
        """Alter an existing products detailes"""
        product = []
        data = request.get_json()
        existing_product = coll.find_one({'name': name})
        if existing_product:
            existing_product['name'] = data.get("name", None)
            existing_product['quantity'] = data.get("quantity", None)
            existing_product['price'] = data.get("price", None)
            product.append({
                "name": existing_product['name'],
                "quantity": existing_product['quantity'],
                "price": existing_product['price']
            })
            coll.save(existing_product)
            return product
        else:
            api.abort(404)
