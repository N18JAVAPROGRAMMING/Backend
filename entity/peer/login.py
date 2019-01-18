import secrets


def sign_in(connection, username, passwd):
    cursor = connection.cursor()
    sql = "SELECT password FROM users WHERE username=%s"
    cursor.execute(sql, (username,))
    if passwd == cursor.fetchone()[0]:
        sql = "UPDATE users SET token=%s WHERE username=%s"
        token = secrets.token_urlsafe(16)
        cursor.execute(sql, (token, username))
        connection.commit()
        cursor.close()
        return token
    else:
        return False
