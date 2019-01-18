from src.token import get_username


def connect_peer(connection, token, room_id):
    peer_name = get_username(connection, token)
    if type(peer_name) == str:
        cursor = connection.cursor()
        sql = "SELECT id, capacity, peer_count, peer_list FROM ROOMS WHERE id=%s"
        cursor.execute(sql, (str(room_id),))
        row = cursor.fetchone()
        if row[1] - row[2] >= 1:
            assert peer_name not in row[3]
            peer_list = row[3] + ";" + str(peer_name)
            sql = "UPDATE rooms SET peer_count=%s, peer_list=%s WHERE id =%s"
            cursor.execute(sql, (str(row[2] + 1), peer_list, str(row[0])))
            connection.commit()
            if row[1] - row[2] > 1:
                return {"prepared": "no"}
            else:
                return {"prepared": "yes"}
        else:
            return False
    else:
        return False
