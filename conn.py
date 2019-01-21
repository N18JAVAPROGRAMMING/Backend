import MySQLdb


class DB:
    conn = None

    def connect(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="task_list", charset='utf8')

    def query(self, *args, **kwargs):
        try:
            cursor = self.conn.cursor()
            cursor.execute(*args, **kwargs)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(*args, **kwargs)
        return cursor

    def commit(self):
        self.conn.commit()
