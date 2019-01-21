from src.token import get_username
from entity.peer.peer_count import count
from time import time


def connect_peer(connection, token, room_id):
    username = get_username(connection, token)
    if type(username) == str:
        sql = "SELECT id, capacity, peer_list FROM rooms WHERE id=%s"
        cur = connection.query(sql, (str(room_id),))
        row = cur.fetchone()
        cur.close()
        if row[1] - count(row[2]) >= 1:
            assert username not in row[2]
            peer_list = row[2] + ";" + str(username)
            sql = "UPDATE rooms SET peer_list = %s WHERE id = %s"
            connection.query(sql, (peer_list, str(row[0])))
            if row[1] - count(row[2]) > 1:
                connection.commit()
                cur.close()
                return {"prepared": "no"}
            else:
                sql = "UPDATE rooms SET time_start = %s WHERE id = %s"
                cur = connection.query(sql, (int(time()), room_id))
                cur.close()
                for w in peer_list.split(";"):
                    sql = "INSERT INTO turnir_table (room_id, username, local_score, solved, non_solved, is_over) " \
                        "VALUES (%s, %s, %s, %s, %s, %s)"
                    cur = connection.query(sql, (room_id, w, 0, 0, 0, 0))
                    connection.commit()
                    cur.close()
                return {"prepared": "yes"}
        else:
            return False
    else:
        return False
