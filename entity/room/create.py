import MySQLdb
from src.token import get_username


def create(connection, token, capacity, room_name):
    initiator = get_username(connection, token)
    if type(initiator) == str:

        try:
                cursor = connection.cursor()
                sql = "INSERT INTO ROOMS (on_start, capacity, room_name, peer_count, peer_list, task_list, is_over) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (str(0), capacity, room_name, str(1), initiator, str(), str(0)))
                connection.commit()
                cursor.close()
                return True
        except MySQLdb.Error:
            return False
    else:
        return False

# SELECT lower_value, upper_value, task_id FROM dominoes JOIN room_task ON(room_task.domino_id = dominoes.id) WHERE room_task.room_id = 3 ;