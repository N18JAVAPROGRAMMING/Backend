from src.token import get_username
from entity.peer.peer_count import count


def disconnect_peer(connection, token, room_id):
    username = get_username(connection, token)
    if type(username) == str:
        cursor = connection.cursor()
        sql = "SELECT id, capacity, peer_list FROM rooms WHERE id=%s"
        cursor.execute(sql, (str(room_id),))
        row = cursor.fetchone()
        if count(row[2]) > 1:
            sql = "UPDATE rooms SET peer_list=%s WHERE id =%s"
            peer_list = row[2].split(';')
            peer_list.remove(str(username))
            cursor.execute(sql, (';'.join(peer_list), str(row[0])))
            connection.commit()
            return True
        elif count(row[2]) == 1 and row[2] == str(username):
            sql = "UPDATE rooms SET peer_list = %s, is_over = %s WHERE id = %s"
            cursor.execute(sql, (str(), str(1), room_id))
            connection.commit()
            return True
    else:
        return False
