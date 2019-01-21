def exists(connection, token):
    sql = "SELECT EXISTS(SELECT token FROM users WHERE token = %s)"
    cur = connection.query(sql, (token,))
    response = cur.fetchone()[0]
    cur.close()
    if response == 1:
        return True
    else:
        return False


def get_username(connection, token):
    sql = "SELECT username FROM users WHERE token = %s"
    cur = connection.query(sql, (token,))
    response = cur.fetchall()[0]
    cur.close()
    if len(response) == 1:
        return response[0]
    else:
        return False
