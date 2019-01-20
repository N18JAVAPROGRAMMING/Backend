from src.token import exists, get_username


def add(connection, token, amt, method):
    if exists(connection, token):
        print(1)
        cursor = connection.cursor()
        username = get_username(connection, token)
        sql = "SELECT local_score, solved, non_solved FROM turnir_table WHERE username=%s AND is_over = 0"
        cursor.execute(sql, (username,))
        raw = cursor.fetchone()
        print(raw)
        data = {"score": raw[0],
                "solved": raw[1],
                "non_solved": raw[2]}

        if method == "1":
            sql = "UPDATE turnir_table SET local_score = %s, solved = %s WHERE username = %s AND is_over = 0"
            cursor.execute(sql, (data['score'] + amt, data['solved'] + 1, username))
        elif method == "2":
            sql = "UPDATE turnir_table SET local_score = %s, non_solved = %s WHERE username = %s AND is_over = 0"
            cursor.execute(sql, (data['score'] - amt, data['non_solved'] + 1, username))

        connection.commit()
        cursor.close()
        return True
    else:
        return False
