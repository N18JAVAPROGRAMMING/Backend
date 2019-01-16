import MySQLdb
import json
from src.token import exists


def get(connection, token,  task_id):
    if exists(connection, token):
        with open('src/tasks/' + task_id + '.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        try:
            cursor = connection.cursor()
            sql = "SELECT answer FROM tasks WHERE id=%s"
            cursor.execute(sql, (task_id,))
            data['ans'] = cursor.fetchone()[0]
            cursor.close()
            return data
        except MySQLdb.Error:
            return False
    else:
        return False
