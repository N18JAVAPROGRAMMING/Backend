from src.token import exists


def status(connection, token, room_id):
    if exists(connection, token):
        sql = "SELECT on_start, capacity, room_name, peer_list FROM rooms WHERE id = %s"
        cur = connection.query(sql, (room_id,))
        row = cur.fetchone()
        response = {"on_start": row[0], "capacity": row[1], "room_name": row[2], "peer_list": row[3].split(";")}
        cur.close()
        return response

    else:
        return False
