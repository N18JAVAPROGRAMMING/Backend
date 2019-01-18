import secrets


def sign_up(connection, username, passwd):
    cursor = connection.cursor()
    sql = "INSERT INTO users (username, password, token) VALUES (%s, %s, %s)"
    token = secrets.token_urlsafe(16)
    cursor.execute(sql, (username, passwd, token))
    connection.commit()
    cursor.close()
    return token
