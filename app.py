import MySQLdb
import json
from flask import Flask, request

import entity.room.create
import entity.room.peerc
import entity.room.info

app = Flask(__name__)
connection = MySQLdb.connect(host="localhost", user="root", passwd="", db="task_list", charset='utf8')


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
    data = request.get_json()
    try:
        if entity.room.peerc.connect(connection, data['room_id'], data['peer_id']):
            return json.dumps({"status": "success"}), 201
        else:
            return json.dumps({"status": "failed"}), 500
    except KeyError:
        return json.dumps({"status": "failed"}), 500


@app.route('/room/info', methods=['GET'])
def check_lobby():
    data = entity.room.info.info(connection)
    if type(data) == list:
        return json.dumps(data), 201
    else:
        return json.dumps({"status": "failed"}), 500


if __name__ == '__main__':
    app.run(debug=True)
