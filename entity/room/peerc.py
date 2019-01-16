import MySQLdb
from src.token import get_username


def connect_peer(connection, token, room_id):
    peer_name = get_username(connection, token)
    if type(peer_name) == str:
        try:
            cursor = connection.cursor()
            sql = "SELECT id, capacity, peer_count, peer_list FROM ROOMS WHERE id=%s"
            cursor.execute(sql, (str(room_id),))
            row = cursor.fetchone()
            if row[1] - row[2] >= 1:
                sql = "UPDATE rooms SET peer_count=%s, peer_list=%s WHERE id =%s"
                cursor.execute(sql, (str(row[2] + 1),
                                     row[3] + ";" + str(peer_name),
                                     str(row[0])))
                connection.commit()
                if row[1] - row[2] > 1:
                    return {"status": "success", "prepared": "no"}
                else:
                    return {"status": "success", "prepared": "yes"}
            else:
                return False
        except MySQLdb.Error:
            return False
    else:
        return False
