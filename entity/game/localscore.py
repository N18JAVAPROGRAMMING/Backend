from src.token import get_username


def add(connection, token, amt, method, task_id):
    username = get_username(connection, token)
    sql = "SELECT local_score, solved, non_solved FROM turnir_table WHERE username=%s AND is_over = 0"
    cur = connection.query(sql, (username,))
    raw = cur.fetchone()
    cur.close()
    data = {"score": raw[0],
            "solved": raw[1],
            "non_solved": raw[2]}

    if method == "1":
        sql = "UPDATE turnir_table SET local_score = %s, solved = %s WHERE username = %s AND is_over = 0"
        cur1 = connection.query(sql, (data['score'] + amt, data['solved'] + 1, username))

        sql = "UPDATE room_task JOIN turnir_table ON room_task.room_id = turnir_table.room_id " \
              "SET room_task.captured = 0, room_task.is_solve = 1 " \
              "WHERE turnir_table.username = %s AND room_task.task_id = %s " \
              "AND room_task.captured = 1 AND room_task.is_solved = 0"
        cur2 = connection.query(sql, (username, task_id))

    elif method == "2":
        sql = "UPDATE turnir_table SET local_score = %s, non_solved = %s WHERE username = %s AND is_over = 0"
        cur1 = connection.query(sql, (data['score'] - amt, data['non_solved'] + 1, username))

        sql = "UPDATE room_task JOIN turnir_table ON room_task.room_id = turnir_table.room_id " \
              "SET room_task.captured = 0 " \
              "WHERE turnir_table.username = %s AND room_task.task_id = %s " \
              "AND room_task.captured = 1 AND room_task.is_solved = 0"
        cur2 = connection.query(sql, (username, task_id))

    assert cur2.rowcount == 1
    connection.commit()
    cur1.close()
    cur2.close()
    return True
