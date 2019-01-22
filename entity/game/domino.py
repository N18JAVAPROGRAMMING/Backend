import json
from src.token import get_username


def capture(connection, token, task_id):
    username = get_username(connection, token)

    sql = "SELECT captured FROM room_task JOIN turnir_table ON(room_task.room_id = turnir_table.room_id) " \
          "WHERE turnir_table.username = %s AND room_task.task_id = %s AND room_task.is_solved = 0"
    cur = connection.query(sql, (username, task_id))
    row = cur.fetchone()
    cur.close()

    assert row[0] == 0
    sql = "UPDATE room_task JOIN turnir_table ON (room_task.room_id = turnir_table.room_id) " \
          "SET room_task.captured = 1 WHERE room_task.task_id = %s AND room_task.is_solved = 0"
    # sql = "UPDATE room_task SET captured = 1 WHERE task_id = %s AND is_solved = 0"
    cur = connection.query(sql, (task_id,))
    connection.commit()
    cur.close()

    with open('src/tasks/' + task_id + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    sql = "SELECT answer FROM tasks WHERE id=%s"
    cur = connection.query(sql, (task_id,))
    data['ans'] = cur.fetchone()[0]
    cur.close()
    return data
