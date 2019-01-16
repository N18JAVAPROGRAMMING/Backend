import MySQLdb
import secrets


def sign_up(connectin, username, passwd):
    try:
        cursor = connectin.cursor()
        sql = "INSERT INTO users (username, password, token) VALUES (%s, %s, %s)"
        token = secrets.token_urlsafe(16)
        cursor.execute(sql, (username, passwd, token))
        connectin.commit()
        cursor.close()
        return token
    except MySQLdb.Error:
        return False
