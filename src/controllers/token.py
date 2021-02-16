from flask import request
from flask_restplus import Resource

from server.instance import server
from services.pix import PixService

api = server.api


@api.route('/token', methods=['POST'])
class Token(Resource):

    def post(self, ):
        pix_service = PixService()
        response = pix_service.get_token()
        return response
