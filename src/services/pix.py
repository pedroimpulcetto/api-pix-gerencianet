
import base64
import requests
import json
import pyqrcode
import png
from io import BytesIO
from PIL import Image
from flask import send_file

from utils.constants import CLIENT_ID, CLIENT_SECRET, CERTIFICADO, URL_ROOT_PROD


class PixService():
    def __init__(self, ):
        self.headers = {
            'Authorization': f'Bearer {self.get_token()}',
            'Content-Type': 'application/json'
        }

    def get_token(self, ):
        auth = base64.b64encode(
            (f"{CLIENT_ID}:{CLIENT_SECRET}").encode()).decode()

        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json'
        }

        payload = {"grant_type": "client_credentials"}

        response = requests.post(
            f'{URL_ROOT_PROD}/oauth/token',
            headers=headers,
            data=json.dumps(payload),
            cert=CERTIFICADO
        )

        return json.loads(response.content)['access_token']

    def create_qrcode(self, location_id):
        response = requests.get(
            f'{URL_ROOT_PROD}/v2/loc/{location_id}/qrcode', headers=self.headers, cert=CERTIFICADO)

        return json.loads(response.content)

    def qrcode_generator(self, location_id):
        qrcode = self.create_qrcode(location_id)
        dados_qrcode = qrcode['qrcode']
        url = pyqrcode.QRCode(dados_qrcode, error='H')
        url.png('test.jpg', scale=10)
        im = Image.open('test.jpg')
        im = im.convert('RGBA')
        img_io = BytesIO()
        im.save(img_io, 'PNG', quality=100)
        img_io.seek(0)

        return send_file(img_io, mimetype='image/jpeg', as_attachment=False, attachment_filename='testeimageqrcod.jpg')

    def create_order(self, txid, payload):

        response = requests.put(f'{URL_ROOT_PROD}/v2/cob/{txid}',
                                data=json.dumps(payload), headers=self.headers, cert=CERTIFICADO)

        if response.status_code == 201:
            return json.loads(response.content)

        return {}

    def create_cobranca(self, txid, payload):
        location_id = self.create_order(txid, payload).get('loc').get('id')
        qrcode = self.qrcode_generator(location_id)
        return qrcode
