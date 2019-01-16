import MySQLdb


def start(connection, room_id):
    return 0


"""
1) log in, username + password; UPDATE token -> token
2) GET room/list?token=fgdsgdfgdfgfg
 SELECT id FROM USER where token = ?; 403
  -> SELECT * FROM ROOM where user_id = id AND WHERE is_over = 0;
"""