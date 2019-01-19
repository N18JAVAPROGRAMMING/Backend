from src.token import exists


def domino_task(connection, token,  room_id):
    if exists(connection, token):
        cursor = connection.cursor()
        sql = "SELECT domino_id, task_id FROM room_task WHERE room_id = %s"
        cursor.execute(sql, (room_id,))
        response = cursor.fetchall()
        data = {}
        for w in response:
            data[w[0]] = w[1]
        return data

    else:
        return False
