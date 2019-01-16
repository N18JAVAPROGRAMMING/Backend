import MySQLdb
import json
from flask import Flask, request

import entity.room.info
import entity.room.create
import entity.room.peerc
import entity.room.peerdc
import entity.room.start
import entity.peer.signup
import entity.peer.login
import entity.game.gettask

app = Flask(__name__)
connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="",
                             db="task_list",
                             charset='utf8')

connection.query('SET GLOBAL connect_timeout=28800')
connection.query('SET GLOBAL wait_timeout=28800')
connection.query('SET GLOBAL interactive_timeout=28800')


@app.route('/room/info', methods=['GET'])
def room_list():
    data = entity.room.info.info(connection, request.args.get("token"))
    if type(data) == list:
        return json.dumps(data, ensure_ascii=False).encode('utf8'), 200
    else:
        return json.dumps({"status": "failed"}), 500


@app.route('/game/get-task', methods=['GET'])
def task_get():
    try:
        data = entity.game.gettask.get(connection,
                                       request.args.get("token"),
                                       request.args.get("task_id"))
        if type(data) == dict:
            return json.dumps(data, ensure_ascii=False).encode('utf8'), 200
        else:
            return json.dumps({"status": "failed"}), 500
    except KeyError:
        return json.dumps({"status": "failed"}), 500


@app.route('/room/create', methods=['POST'])
def room_create():
    data = request.get_json()
    try:
        if entity.room.create.create(connection, data['token'],
                                     data['capacity'], data['room_name']):
            return json.dumps({"status": "success"}), 200
        else:
            return json.dumps({"status": "failed"}), 500
    except KeyError:
        return json.dumps({"status": "failed"}), 500


@app.route('/room/connect', methods=['POST'])
def peer_connect():
    try:
        data = entity.room.peerc.connect_peer(connection,
                                              request.get_json()['token'],
                                              request.get_json()['room_id'])
        if type(data) == dict:
            return json.dumps(data), 200
        else:
            return json.dumps({"status": "failed"}), 500
    except KeyError:
        return json.dumps({"status": "failed"}), 500


@app.route('/room/disconnect', methods=['POST'])
def peer_disconnect():
    try:
        if entity.room.peerdc.disconnect_peer(connection,
                                              request.get_json()['token'],
                                              request.get_json()['room_id']):
            return json.dumps({"status": "success"}), 200
        else:
            return json.dumps({"status": "failed"}), 500
    except KeyError:
        return json.dumps({"status": "failed"}), 500


@app.route('/room/start', methods=['POST'])
def room_start():
    data = entity.room.start.start(connection, request.get_json()['room_id'])
    try:
        if type(data) == dict:
            return json.dumps(data), 200
        else:
            return json.dumps({"status": "failed"}), 500
    except KeyError:
        return json.dumps({"status": "failed"}), 500


@app.route('/peer/signup', methods=['POST'])
def sign_up():
    try:
        data = entity.peer.signup.sign_up(connection,
                                          request.get_json()['username'],
                                          request.get_json()['password'])
        if type(data) == str:
            return json.dumps({"status": "success", "token": data}), 200
        else:
            return json.dumps({"status": "failed"}), 500
    except KeyError:
        return json.dumps({"status": "failed"}), 500


@app.route('/peer/login', methods=['POST'])
def sign_in():
    try:
        data = entity.peer.login.sign_in(connection,
                                         request.get_json()['username'],
                                         request.get_json()['password'])
        if type(data) == str:
            return json.dumps({"status": "success", "token": data}), 200
        else:
            return json.dumps({"status": "failed"}), 500
    except KeyError:
        return json.dumps({"status": "failed"}), 500


if __name__ == '__main__':
    app.run(debug=True)
