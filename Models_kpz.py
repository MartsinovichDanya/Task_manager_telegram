class InnModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS inn_table
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             inn VARCHAR(50)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, inn):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO inn_table
                          (inn) 
                          VALUES (?)''',
                       (inn, ))
        cursor.close()
        self.connection.commit()

    def get(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM inn_table WHERE id = ?", (str(id),))
        row = cursor.fetchone()
        if not row:
            return False
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM inn_table")
        rows = cursor.fetchall()
        return rows

    def delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM inn_table WHERE id = ?''', (str(id),))
        cursor.close()
        self.connection.commit()


class KpzTaskModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     description VARCHAR(200),
                                     done BOOL,
                                     user_link VARCHAR(100),
                                     file_id INTEGER
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, description, user_link, done=False, file_id=-1):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO tasks 
                                  (description, done, user_link, file_id) 
                                  VALUES (?,?,?,?)''',
                       (description, done, user_link, file_id,))
        cursor.close()
        self.connection.commit()

    def get(self, tid):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (str(tid),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        return rows

    def delete(self, tid):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM tasks WHERE id = ?''', (str(tid),))
        cursor.close()
        self.connection.commit()


class FileModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS files
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             tg_id VARCHAR(200),
                             file_name VARCHAR(200)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, tg_id, file_name):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO files
                          (tg_id, file_name) 
                          VALUES (?,?)''',
                       (tg_id, file_name, ))
        cursor.close()
        self.connection.commit()

    def get(self, fid):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM files WHERE id = ?", (str(fid),))
        row = cursor.fetchone()
        if not row:
            return False
        return row

    def get_id(self, tg_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM files WHERE tg_id = ?", (tg_id, ))
        row = cursor.fetchone()
        return row[0]

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM files")
        rows = cursor.fetchall()
        return rows

    def delete(self, fid):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM files WHERE id = ?''', (str(fid),))
        cursor.close()
        self.connection.commit()
