import MySQLdb
from src.token import exists
from random import sample


def start(connection, token, room_id):
    if exists(connection, token):
        try:
            cursor = connection.cursor()
            data = {}
            for w in range(1, 5):
                sql = "SELECT id FROM tasks WHERE complexity = %s"
                cursor.execute(sql, (w,))
                data[w] = [w for i in cursor.fetchall() for w in i]
#            print(data[2])

            print(sample(data[2], 1))

            cursor.close()
        except MySQLdb.Error:
            return False
    else:
        return False


"""
1) log in, username + password; UPDATE token -> token
2) GET room/list?token=fgdsgdfgdfgfg
 SELECT id FROM USER where token = ?; 403
  -> SELECT * FROM ROOM where user_id = id AND WHERE is_over = 0;
"""