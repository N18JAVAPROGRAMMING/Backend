import secrets


def sign_in(connection, username, passwd):
    sql = "SELECT password FROM users WHERE username=%s"
    cur = connection.query(sql, (username,))
    if passwd == cur.fetchone()[0]:
        cur.close()
        sql = "UPDATE users SET token=%s WHERE username=%s"
        token = secrets.token_urlsafe(16)
        cur = connection.query(sql, (token, username))
        connection.commit()
        cur.close()
        return token
    else:
        cur.close()
        return False
