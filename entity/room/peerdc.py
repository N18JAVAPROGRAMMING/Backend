import MySQLdb


def disconnect_peer(connection, room_id, peer_name):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, capacity, peer_count, peer_list FROM ROOMS WHERE id=%s"
            cursor.execute(sql, (str(room_id),))
            row = cursor.fetchone()
            print(row)
            if row[2] > 1:
                sql = "UPDATE rooms SET peer_count=%s, peer_list=%s WHERE id =%s"
                peer_list = row[3].split(';')
                peer_list.remove(str(peer_name))
                cursor.execute(sql, (str(row[2]-1), ';'.join(peer_list), str(row[0])))
                connection.commit()
                return True

            elif row[2] == 1 and row[3] == str(peer_name):
                print('На удаление')
                sql = "DELETE FROM rooms WHERE id=%s"
                cursor.execute(sql, (str(row[0]),))
                connection.commit()
                return True
    except MySQLdb.Error:
        return False
