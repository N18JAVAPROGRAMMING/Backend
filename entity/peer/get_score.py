from src.token import exists


def get(connection, token, username):
    if exists(connection, token):
        cursor = connection.cursor()
        sql = "SELECT score FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        data = {"score": cursor.fetchone()[0]}
        cursor.close()
        return data
    else:
        return False
