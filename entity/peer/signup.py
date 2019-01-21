import secrets


def sign_up(connection, username, passwd):
    sql = "INSERT INTO users (username, password, token, score) VALUES (%s, %s, %s, %s)"
    token = secrets.token_urlsafe(16)
    cur = connection.query(sql, (username, passwd, token, 0))
    connection.commit()
    cur.close()
    return token
