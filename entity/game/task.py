from src.token import exists


def check(connection, token, room_id):
    if exists(connection, token):
        sql = "SELECT domino_id, captured FROM room_task WHERE room_id = %s"
        cur = connection.query(sql, (room_id,))
        response = cur.fetchall()
        cur.close()
        domino_data = []
        room_data = []
        for w in response:
            domino_data.append(w[0])
            room_data.append(w[1])
        return {
            "dominoes": domino_data,
            "task_status": room_data
        }

    else:
        return False
