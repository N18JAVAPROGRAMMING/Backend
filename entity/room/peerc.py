import MySQLdb


def connect(connection, room_id, peer_id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM ROOMS WHERE id=%s"
            cursor.execute(sql, room_id)
            row = cursor.fetchone()

            cursor.execute("REPLACE INTO ROOMS VALUES ()")
            return
    except MySQLdb.Error:
        return False