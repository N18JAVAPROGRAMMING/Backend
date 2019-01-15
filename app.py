import MySQLdb
import json
from flask import Flask, request

import entity.room.create
import entity.room.peerc
import entity.room.peerdc
import entity.room.info


app = Flask(__name__)
connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="",
                             db="task_list",
                             charset='utf8',
                             connect_timeout=1000)

connection.query('SET GLOBAL connect_timeout=28800')
connection.query('SET GLOBAL wait_timeout=28800')
connection.query('SET GLOBAL interactive_timeout=28800')


@app.route('/room/create', methods=['POST'])
def create_room():
    data = request.get_json()
    try:
        if entity.room.create.create(connection, data['capacity'], data['room_name'], data['initiator']):
            return json.dumps({"status": "success"}), 201
        else:
            return json.dumps({"status": "failed"}), 500
    except KeyError:
        return json.dumps({"status": "failed"}), 500


@app.route('/room/peer-connect', methods=['POST'])
def connect_peer():
    try:
        data = entity.room.peerc.connect_peer(connection,
                                              request.get_json()['room_id'],
                                              request.get_json()['peer_name'])
        if type(data) == dict:
            return json.dumps(data), 201
        else:
            return json.dumps({"status": "failed"}), 500
    except KeyError:
        return json.dumps({"status": "failed"}), 500


@app.route('/room/peer-disconnect', methods=['POST'])
def disconnect_peer():
    try:
        if entity.room.peerdc.disconnect_peer(connection,
                                              request.get_json()['room_id'],
                                              request.get_json()['peer_name']):
            return json.dumps({"status": "success"}), 201
        else:
            return json.dumps({"status": "failed"}), 500
    except KeyError:
        return json.dumps({"status": "failed"}), 500


@app.route('/room/info', methods=['GET'])
def check_lobby():
    data = entity.room.info.info(connection)
    if type(data) == list:
        return json.dumps(data, ensure_ascii=False).encode('utf8'), 200
    else:
        return json.dumps({"status": "failed"}), 500


if __name__ == '__main__':
    app.run(debug=True)
