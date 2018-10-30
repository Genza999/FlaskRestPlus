from flask_restplus import Namespace, fields


class InventoryDto:
    api = Namespace('Inventory', description='Inventory related operations')
    product = api.model('Product_detailes', {
        'name': fields.String(required=True, description='Product Name'),
        'quantity': fields.String(required=True, description='Product quantity'),
        'price': fields.Integer(required=True, description='Product price')
    })
