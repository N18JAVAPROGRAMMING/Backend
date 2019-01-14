import MySQLdb
import json


def info(connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, on_start, capacity, room_name, peer_count FROM ROOMS"
            cursor.execute(sql)
            data = []
            for row in cursor.fetchall():
                data.append({"id": row[0],
                             "on_start": row[1],
                             "capacity": row[2],
                             "room_name": row[3],
                             "peer_count": row[4]})
            return data
    except MySQLdb.Error:
        return False
