import unittest
import json
from flask import Flask
from flask import request, jsonify, make_response
from flask_restplus import Resource
from pymongo import MongoClient
from base64 import b64encode
from manage import app


class APITestCase(unittest.TestCase):

    def setUp(self):
        MdbURI = 'mongodb://user0:countries9@ds145463.mlab.com:45463/sayuni_db'
        client = MongoClient(MdbURI)
        db = client['sayuni_db']
        coll = db.inventory
        self.client = app.test_client()

    def tearDown(self):
        pass

    def get_api_headers(self):
        return {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_get_products(self):
        '''Testing GET request of all products'''
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['data'][0]['name'], 'Gloves')

    def test_single_product(self):
        '''Testing POST, GET, PUT, DELETE request of a single product'''
        response = self.client.post(
            '/inventory/',
            headers=self.get_api_headers(),
            data=json.dumps({"name": "carpets", "quantity": "1dz", "price": 60000}))
        self.assertEqual(response.status_code, 201)

        '''Creating a product that already exists'''
        response = self.client.post(
            '/inventory/',
            headers=self.get_api_headers(),
            data=json.dumps({"name": "carpets", "quantity": "1dz", "price": 60000}))
        self.assertEqual(response.status_code, 200)

        '''Testing GET request for the product created'''
        response = self.client.get(
            '/inventory/carpets')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['name'], 'carpets')

        '''Testing PUT request for the created product'''
        response = self.client.put(
            '/inventory/carpets',
            headers=self.get_api_headers(),
            data=json.dumps({"name": "carpets", "quantity": "10dz", "price": 120000}))
        self.assertEqual(response.status_code, 200)

        '''Testing DELETE request for the created product'''
        response = self.client.delete(
            '/inventory/carpets')
        self.assertEqual(response.status_code, 201)

        '''Testing DELETE request for a product that dsnt exist'''
        response = self.client.delete(
            '/inventory/garments')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'garments not found' in response.get_data(
                as_text=True))


if __name__ == '__main__':
    unittest.main()
