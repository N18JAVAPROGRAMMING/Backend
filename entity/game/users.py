from src.token import exists


def info(connection, token, room_id):
    assert exists(connection, token)
    sql = "SELECT username, local_score, solved, non_solved FROM turnir_table WHERE room_id = %s"
    cur = connection.query(sql, (room_id,))
    row = cur.fetchall()
    cur.close()
    username_data = []
    score_data = []
    for w in row:
        username_data.append(w[0])
        score_data.append(w[1:])

    return {
        "users_data": username_data,
        "score_data": score_data
    }
