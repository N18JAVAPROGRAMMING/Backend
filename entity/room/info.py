from src.token import exists
from entity.peer.peer_count import count


def info(connection, token):
    if exists(connection, token):
        cursor = connection.cursor()
        sql = "SELECT id, on_start, capacity, room_name, peer_list FROM rooms WHERE is_over = 0"
        cursor.execute(sql)
        data = []
        for row in cursor.fetchall():
            data.append({"id": row[0],
                         "on_start": row[1],
                         "capacity": row[2],
                         "room_name": row[3],
                         "peer_count": count(row[4])})
        cursor.close()
        return data
    else:
        return False
