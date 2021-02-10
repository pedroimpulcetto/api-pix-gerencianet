from flask import request
from flask_restplus import Api, Resource, fields

from server.instance import server
from services.pix import PixService

api = server.api



@api.route('/orders', methods=['POST'])
class Pix(Resource):

    def post(self, ):
        data = request.json
        txid = data.pop('txid')

        pix_service = PixService()
        response = pix_service.create_cobranca(txid, data)
        return response

    