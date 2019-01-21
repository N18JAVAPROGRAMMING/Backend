from src.token import exists


def get(connection, token, username):
    if exists(connection, token):
        sql = "SELECT score FROM users WHERE username = %s"
        cur = connection.query(sql, (username,))
        data = {"score": cur.fetchone()[0]}
        cur.close()
        return data
    else:
        return False
