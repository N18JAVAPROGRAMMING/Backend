from src.token import exists


def domino_task(connection, token,  room_id):
    if exists(connection, token):
        sql = "SELECT domino_id, task_id FROM room_task WHERE room_id = %s"
        cur = connection.query(sql, (room_id,))
        response = cur.fetchall()
        cur.close()
        domino_data = []
        task_data = []
        for w in response:
            domino_data.append(w[0])
            task_data.append(w[1])
        return {
            "dominoes": domino_data,
            "tasks": task_data
        }

    else:
        return False
