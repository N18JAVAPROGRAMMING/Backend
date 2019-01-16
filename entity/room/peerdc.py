import MySQLdb
from src.token import get_username


def disconnect_peer(connection, token, room_id):
    peer_name = get_username(connection, token)
    if type(peer_name) == str:
        try:
            cursor = connection.cursor()
            sql = "SELECT id, capacity, peer_count, peer_list FROM ROOMS WHERE id=%s"
            cursor.execute(sql, (str(room_id),))
            row = cursor.fetchone()
            if row[2] > 1:
                sql = "UPDATE rooms SET peer_count=%s, peer_list=%s WHERE id =%s"
                peer_list = row[3].split(';')
                peer_list.remove(str(peer_name))
                cursor.execute(sql, (str(row[2] - 1), ';'.join(peer_list), str(row[0])))
                connection.commit()
                return True
            elif row[2] == 1 and row[3] == str(peer_name):
                sql = "UPDATE rooms SET peer_list=%s, is_over=%s WHERE id=%s"
                cursor.execute(sql, (str(), str(1), room_id))
                connection.commit()
                return True
        except MySQLdb.Error:
            return False
    else:
        return False
