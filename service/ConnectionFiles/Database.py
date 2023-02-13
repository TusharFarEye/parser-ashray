import psycopg2


class Database:

    def __init__(self, hostname, database, username, pwd, port_id):
            self.conn = psycopg2.connect(
                            host = hostname,
                            dbname = database,
                            user = username,
                            password = pwd,
                            port = port_id)

            self.cur = self.conn.cursor()

    def get_cursor(self):
        return self.cur

    def get_connection(self):
        return self.conn
