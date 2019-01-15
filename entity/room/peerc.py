import MySQLdb


def connect_peer(connection, room_id, peer_name):
    cursor = connection.cursor()
    sql = "SELECT id, capacity, peer_count, peer_list FROM ROOMS WHERE id=%s"
    try:
        cursor.execute(sql, (str(room_id),))
        row = cursor.fetchone()
        if row[1] - row[2] >= 1:
            try:
                sql = "UPDATE rooms SET peer_count=%s, peer_list=%s WHERE id =%s"
                cursor.execute(sql, (str(row[2] + 1),
                                     row[3] + ";" + str(peer_name),
                                     str(row[0])))
                connection.commit()
                if row[1] - row[2] > 1:
                    return {"status": "success", "prepared": "no"}
                else:
                    return {"status": "success", "prepared": "yes"}
            except MySQLdb.Error:
                return False
        else:
            return False
    except MySQLdb.Error:
        return False
