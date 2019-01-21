import MySQLdb
from flask import Flask, request, jsonify

import conn
import entity.room.info
import entity.room.status
import entity.room.create
import entity.room.peerc
import entity.room.peerdc
import entity.peer.signup
import entity.peer.login
import entity.peer.get_score
import entity.game.domino
import entity.game.dependencies
import entity.game.localscore
import src.token

app = Flask(__name__)

connection = conn.DB()
connection.query('SET GLOBAL connect_timeout=28800')
connection.query('SET GLOBAL wait_timeout=28800')
connection.query('SET GLOBAL interactive_timeout=28800')


@app.route('/room/info', methods=['GET'])
def room_list():
    try:
        data = entity.room.info.info(connection, request.args.get("token"))
        if type(data) == list:
            return jsonify(data), 200
        else:
            return jsonify({"status": "failed"}), 500
    except:
        return jsonify({"status": "failed"}), 500


@app.route('/token/check', methods=['GET'])
def token_exists():
    try:
        if src.token.exists(connection, request.args.get("token")):
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "failed"}), 500
    except:
        return jsonify({"status": "failed"}), 500


@app.route('/room/status', methods=['GET'])
def status():
    try:
        data = entity.room.status.status(connection,
                                         request.args.get("token"),
                                         request.args.get("room_id"))
        if type(data) == dict:
            return jsonify(data), 200
        else:
            return jsonify({"status": "failed"}), 500
    except:
        return jsonify({"status": "failed"}), 500


@app.route('/peer/score', methods=['GET'])
def peer_score():
    try:
        data = entity.peer.get_score.get(connection,
                                         request.args.get("token"),
                                         request.args.get("username"))
        if type(data) == dict:
            return jsonify(data), 200
        else:
            return jsonify({"status": "failed"}), 500
    except Exception as ex:
        print(ex)
        return jsonify({"status": "failed"}), 500


@app.route('/game/dependencies', methods=['GET'])
def domino_task():
    try:
        data = entity.game.dependencies.domino_task(connection,
                                                    request.args.get("token"),
                                                    request.args.get("room_id"))
        if type(data) == dict:
            return jsonify(data), 200
        else:
            return jsonify({"status": "failed"}), 500
    except:
        return jsonify({"status": "failed"}), 500


@app.route('/game/domino', methods=['POST'])
def domino_capture():
    try:
        data = entity.game.domino.capture(connection,
                                          request.get_json()["token"],
                                          request.get_json()["task_id"])
        if type(data) == dict:
            return jsonify(data), 200
        else:
            return jsonify({"status": "failed"}), 500
    except Exception as ex:
        print(ex)
        return jsonify({"status": "failed"}), 500


@app.route('/game/score', methods=['POST'])
def add_local_score():
    try:
        data = request.get_json()
        if entity.game.localscore.add(connection, data["token"], int(data["amt"]),
                                      str(data["method"]), data["task_id"]):
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "failed"}), 500
    except Exception as ex:
        print(ex)
        return jsonify({"status": "failed"}), 500


@app.route('/room/create', methods=['POST'])
def room_create():
        data = request.get_json()

        room_id = entity.room.create.create(connection, data['token'], data['capacity'],
                                            data['room_name'], int(data['domino_amt']))
        if type(room_id) == int:
            data = entity.room.status.status(connection, data['token'], room_id)
            data["id"] = room_id
            return jsonify(data), 200
        else:
            return jsonify({"status": "failed"}), 500



@app.route('/room/connect', methods=['POST'])
def peer_connect():
    try:
        data = request.get_json()
        response = entity.room.peerc.connect_peer(connection, data['token'], data['room_id'])
        if type(response) == dict:
            return jsonify(entity.room.status.status(connection, data['token'], data['room_id'])), 200
        else:
            return jsonify({"status": "failed"}), 500
    except Exception as ex:
        print(ex)
        return jsonify({"status": "failed"}), 500


@app.route('/room/disconnect', methods=['POST'])
def peer_disconnect():
    try:
        data = request.get_json()
        if entity.room.peerdc.disconnect_peer(connection, data['token'], data['room_id']):
            response = entity.room.info.info(connection, data['token'])
            return jsonify(response), 200
        else:
            return jsonify({"status": "failed"}), 500
    except:
        return jsonify({"status": "failed"}), 500


@app.route('/peer/signup', methods=['POST'])
def sign_up():
    try:
        data = entity.peer.signup.sign_up(connection,
                                          request.get_json()['username'],
                                          request.get_json()['password'])
        if type(data) == str:
            return jsonify({"token": data}), 200
        else:
            return jsonify({"status": "failed"}), 500
    except:
        return jsonify({"status": "failed"}), 500


@app.route('/peer/login', methods=['POST'])
def sign_in():
    try:
        data = entity.peer.login.sign_in(connection,
                                         request.get_json()['username'],
                                         request.get_json()['password'])
        if type(data) == str:
            return jsonify({"token": data}), 200
        else:
            return jsonify({"status": "failed"}), 500
    except Exception as ex:
        print(ex)
        return jsonify({"status": "failed"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
