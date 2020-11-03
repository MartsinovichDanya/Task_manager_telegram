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
