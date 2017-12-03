from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import os
import json
import pymysql
import requests
import subprocess
import grequests

app = Flask(__name__)
api = Api(app)

devices = ['143.248.226.19', '143.248.229.39']
#devices = ['127.0.0.1', '127.0.0.1']

@app.route('/')
def hello():
    return 'Hello World!'

#@app.route('/kommand', methods = ['POST'])
#def kommand():
#    if request.method == "POST":
#        print (request)
#        print (request.get_json())
#        json_dict = request.get_json()
#        kommand_input = json_dict['kommand_input']
#        kommand_output = os.popen(kommand_input).read()
#        #kommand_output = run(kommand_parser(kommand_input), stdout=PIPE, stderr=PIPE, universal_newlines=True)
#        #print (kommand_output.stdout)
#        #data = {'kommand_output': kommand_output.stdout}
#        data = {'kommand_output': kommand_output}
#        return jsonify(data)

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == "POST":
        print (3)
        print (request)
        print (request.get_json())
        file_info = json.loads(request.get_json())
        conn = pymysql.connect(host='localhost', user='root', password='root', db='CS408', charset='utf8')
        curs = conn.cursor()
        sql = """insert into file(file_name, file_block_name, file_block_index, saved_device_address, file_size, block_size) values (%s, %s, %s, %s, %s, %s)"""
        for i in range(len(file_info['file_block_name'])):
            for j in range(len(devices)):
                os.system("sshpass -p 'changeme' scp ~/disk_cold/"+file_info['file_block_name'][i]+" android@"+devices[j]+":~/disk_cold/.")
                curs.execute(sql, (file_info['file_name'], file_info['file_block_name'][i], i, devices[j], int(file_info['file_size']), int(file_info['block_size'][i])))
                print (i, j)
        #curs.execute(sql, ('a', 'aa', int(0), '127.0.0.1', int(0), int(0)))
        conn.commit()
        conn.close()
        print ('commit and close')
        data = {'message': 'success'}
        return jsonify(data)

@app.route('/download', methods = ['POST']) # JSON { 'file_name': string } 
def download():
    if request.method == "POST":
        file_info = json.loads(request.get_json())
        conn = pymysql.connect(host='localhost', user='root', password='root', db='CS408', charset='utf8')
        curs = conn.cursor()
        sql = "select file_block_name, file_block_index, saved_device_address from file where file_name = '"+file_info['file_name']+"'"
        curs.execute(sql)
        rows = curs.fetchall()
        print (rows)
        print (rows[0][0].strip(), rows[1][0].strip(), str(rows[0][1]), str(rows[1][1]))
        alive_devices = []
        for i in range(len(devices)):
            response = os.system("ping -c 1 " + devices[i])
            if response == 0:
                alive_devices.append(devices[i])
        unused_indexes = [0,1]
        urls = []
        datas = []
        if len(alive_devices) == 2:
            for i in range(len(rows)):
                if rows[i][1] in unused_indexes and rows[i][2].strip() in alive_devices:
                    file_info2 = '{"file_block_name": "'+rows[i][0].strip()+'", "file_block_index": '+str(rows[i][1])+', "client_address": "'+file_info['client_address']+'", "client_id": "'+file_info['client_id']+'", "client_pw": "'+file_info['client_pw']+'"}'
                    datas.append(file_info2)
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    url = 'http://'+rows[i][2].strip()+':5000/download_relay'
                    urls.append(url)
                    #response2 = requests.post(url, data=json.dumps(file_info2), headers = headers)
                    unused_indexes.remove(rows[i][1])
                    alive_devices.remove(rows[i][2].strip())
        elif len(alive_devices) == 1:
            for i in range(len(rows)):
                if rows[i][1] in unused_indexes and rows[i][2].strip() in alive_devices:
                    file_info2 = '{"file_block_name": "'+rows[i][0].strip()+'", "file_block_index": '+str(rows[i][1])+', "client_address": "'+file_info['client_address']+'", "client_id": "'+file_info['client_id']+'", "client_pw": "'+file_info['client_pw']+'"}'
                    datas.append(file_info2)
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    url = 'http://'+rows[i][2].strip()+':5000/download_relay'
                    urls.append(url)
                    #response2 = requests.post(url, data=json.dumps(file_info2), headers = headers)
                    unused_indexes.remove(rows[i][1])
        rs = (grequests.post(urls[k], data = datas[k]) for k in range(len(urls)))
        print (grequests.map(rs))
        conn.close()
        data = {'message': 'success'}
        return jsonify(data)

@app.route('/download_relay', methods = ['POST'])
def download_relay():
    if request.method == "POST":
        file_info = json.loads(request.get_json())
        print ("HOLY COW")
        #subprocess.call(["sshpass -p "+file_info['client_pw']+" scp -o StrictHostKeyChecking=no ~/disk_cold/"+file_info['file_block_name']+" "+file_info['client_id']+"@"+file_info['client_address']+":~/."], shell=True)
        #curs.execute(sql, ('a', 'aa', int(0), '127.0.0.1', int(0), int(0)))
        data = {'message': 'success'}
        return jsonify(data)
if __name__ == '__main__':
    app.run(host='0.0.0.0')

