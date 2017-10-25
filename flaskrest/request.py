import requests
import simplejson as json
'''
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

if __name__=='__main__':
	app.run(host='0.0.0.0')
'''
url = 'http://172.17.0.2:5000/kommand' #IP address of other machine
while(True):
	kommand_input = input("Input Kommand:")
	data = {'kommand_input': kommand_input}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} 
	response = requests.post(url, data=json.dumps(data), headers = headers)
	json_dict = response.json()
	print (json_dict.get('kommand_output'))
