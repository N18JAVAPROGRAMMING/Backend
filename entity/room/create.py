from src.token import get_username
from random import sample


def create(connection, token, capacity, room_name, domino_amt):
    def tasks_sort(w):
        return w[1]

    def dominoes_sort(w):
        s = sum(w[1:])
        if 1 <= s <= 5:
            return 1
        elif 6 <= s <= 7:
            return 2
        elif 8 <= s <= 9:
            return 3
        else:
            return 4

    assert 1 <= domino_amt <= 28
    initiator = get_username(connection, token)

    if type(initiator) == str:

        sql = "INSERT INTO rooms (on_start, capacity, room_name, peer_list, domino_amt, is_over) " \
              "VALUES (%s, %s, %s, %s, %s, %s)"
        cur = connection.query(sql, (str(0), capacity, room_name, initiator, domino_amt, str(0)))
        room_id = connection.conn.insert_id()
        connection.commit()
        cur.close()

        sql = "SELECT id, complexity FROM tasks"
        cur = connection.query(sql)
        data_tasks = sample(cur.fetchall(), domino_amt)
        data_tasks.sort(key=tasks_sort)
        cur.close()

        sql = "SELECT * FROM dominoes"
        cur = connection.query(sql)
        data_dominoes = sample(cur.fetchall(), domino_amt)
        data_dominoes.sort(key=dominoes_sort)
        cur.close()

        for w in range(domino_amt):
            sql = "INSERT INTO room_task (room_id, domino_id, task_id, captured, solved, non_solved, is_solved) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur = connection.query(sql, (room_id, data_dominoes[w][0], data_tasks[w][0], 0, 0, 0, 0))
            connection.commit()
            cur.close()
        return room_id

    else:
        return False

# SELECT lower_value, upper_value, task_id FROM dominoes JOIN room_task ON(room_task.domino_id = dominoes.id) WHERE room_task.room_id = 3 ;
