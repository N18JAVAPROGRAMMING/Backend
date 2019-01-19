from src.token import get_username
from entity.peer.peer_count import count


def connect_peer(connection, token, room_id):
    username = get_username(connection, token)
    if type(username) == str:
        cursor = connection.cursor()
        sql = "SELECT id, capacity, peer_list FROM rooms WHERE id=%s"
        cursor.execute(sql, (str(room_id),))
        row = cursor.fetchone()
        if row[1] - count(row[2]) >= 1:
            assert username not in row[2]
            peer_list = row[2] + ";" + str(username)
            sql = "UPDATE rooms SET peer_list = %s WHERE id = %s"
            cursor.execute(sql, (peer_list, str(row[0])))
            connection.commit()
            if row[1] - count(row[2]) > 1:
                return {"prepared": "no"}
            else:
                return {"prepared": "yes"}
        else:
            return False
    else:
        return False
