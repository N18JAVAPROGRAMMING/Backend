import MySQLdb


def info(connection):
    with connection.cursor() as cursor:
        try:
            sql = "SELECT id, on_start, capacity, room_name, peer_count FROM rooms"
            cursor.execute(sql)
            data = []
            for row in cursor.fetchall():
                data.append({"id": row[0],
                             "on_start": row[1],
                             "capacity": row[2],
                             "room_name": row[3],
                             "peer_count": row[4]})
            cursor.close()
            return data
        except MySQLdb.Error:
            return False
