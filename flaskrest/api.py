from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import os
import json
import pymysql

app = Flask(__name__)
api = Api(app)

conn = pymysql.connect(host='localhost', user='root', password='root', db='CS408', charset='utf8')

@app.route('/')
def hello():
    return 'Hello World!'

#@app.route('/kommand', methods = ['POST'])
#def kommand():
#	if request.method == "POST":
#		print (request)
#		print (request.get_json())
#		json_dict = request.get_json()
#		kommand_input = json_dict['kommand_input']
#		kommand_output = os.popen(kommand_input).read()
#		#kommand_output = run(kommand_parser(kommand_input), stdout=PIPE, stderr=PIPE, universal_newlines=True)
#		#print (kommand_output.stdout)
#		#data = {'kommand_output': kommand_output.stdout}
#		data = {'kommand_output': kommand_output}
#		return jsonify(data)

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == "POST":
        file_info = json.loads(request.get_json())
        print (file_info)
        print (int(file_info['file_size']))
        print (int(file_info['block_size'][0]))
        conn = pymysql.connect(host='localhost', user='root', password='root', db='CS408', charset='utf8')
        curs = conn.cursor()
        sql = """insert into file(file_name, file_block_name, file_block_index, saved_device_address, file_size, block_size) values (%s, %s, %s, %s, %s, %s)"""
        curs.execute(sql, (file_info['file_name'], file_info['file_block_name'][0], 0, '127.0.0.1', int(file_info['file_size']), int(file_info['block_size'][0])))
        #curs.execute(sql, ('a', 'aa', int(0), '127.0.0.1', int(0), int(0)))
        conn.commit()
        conn.close()
        data = {'message': 'success'}
        return jsonify(data)


def kommand_parser(kommand_input):
    return kommand_input.split()


if __name__ == '__main__':
    app.run(host='0.0.0.0')

