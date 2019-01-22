from src.token import exists
from time import time


def over(connection, token, room_id):
    assert exists(connection, token)
    sql = "SELECT time_start, domino_amt FROM rooms WHERE id = %s"
    cur = connection.query(sql, (room_id,))
    row = cur.fetchone()
    cur.close()
    if row[1] <= 14:
        assert int(time()) - row[0] > 14 * 60
    elif row[1] > 14:
        assert int(time()) - row[0] > 28 * 60
    sql = "SELECT username FROM turnir_table WHERE room_id = %s"
    cur = connection.query(sql, (room_id,))
    row = cur.fetchall()
    cur.close()
    for w in row:
        sql = "SELECT local_score FROM turnir_table WHERE username = %s AND room_id = %s"
        cur = connection.query(sql, (w[0], room_id))
        ls = cur.fetchone()[0]
        cur.close()

        sql = "SELECT score FROM users WHERE username = %s"
        cur = connection.query(sql, (w[0],))
        gs = cur.fetchone()[0]
        cur.close()

        sql = "UPDATE users SET score = %s WHERE username = %s"
        cur = connection.query(sql, (gs + ls, w[0]))
        cur.close()

    sql = "UPDATE turnir_table SET local_score = 0, is_over = 1 WHERE room_id = %s"
    cur1 = connection.query(sql, (room_id,))

    sql = "UPDATE room_task SET is_solved = 1 WHERE room_id = %s"
    cur2 = connection.query(sql, (room_id,))

    connection.commit()
    cur1.close()
    cur2.close()
    return True
