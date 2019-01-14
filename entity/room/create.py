import MySQLdb


def create(connection, capacity, room_name, initiator):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO ROOMS (on_start, capacity, room_name, peer_count, peer_list, task_list) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (str(0), capacity, room_name, str(1), initiator, str()))
            connection.commit()
            return True
    except MySQLdb.Error:
        return False

