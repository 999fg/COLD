import requests
import json
'''
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

if __name__=='__main__':
	app.run(host='0.0.0.0')
'''
url = 'http://143.248.225.40:5000/' #IP address of other machine
while(True):
        print ('Client -> Control Plane, /upload (POST) : 1')
        rest_choice = input()
        if int(rest_choice) == 1:
                url = url + 'upload'
                file_info = '{"file_name": "earth.jpg", "file_block_name": ["file1.jpg", "file2.jpg"], "file_size": 10000000, "block_size": [500000, 500000]}'
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                response = requests.post(url, data=json.dumps(file_info), headers = headers)
                json_dict = response.json()
                print (json_dict.get('message'))

        if int(rest_choice) == 2:
                url = url + 'download'
                file_info = '{"file_name": "earth.jpg"}'
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                response = requests.post(url, data=json.dumps(file_info), headers = headers)
                json_dict = response.json()
                print (json_dict.get('message'))

