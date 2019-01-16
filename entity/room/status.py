import MySQLdb
from src.token import exists


def status(connection, token, room_id):
    if exists(connection, token):
        try:
            cursor = connection.cursor()
            sql = "SELECT on_start, capacity, room_name, peer_list FROM rooms WHERE id=%s"
            cursor.execute(sql, (room_id,))
            row = cursor.fetchone()
            response = {"on_start": row[0], "capacity": row[1], "room_name": row[2], "peer_count": row[3].split(";")}
            cursor.close()
            return response
        except MySQLdb.Error:
            return False
    else:
        return False
