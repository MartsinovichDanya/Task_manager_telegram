class UserModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             tg_id INTEGER,
                             boss BOOL
                             )''')
        cursor.close()
        self.connection.commit()

    def make_boss(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users SET 
                            boss = ?
                            WHERE id = ?''', (True, str(user_id)))
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, tg_id, boss=False):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, tg_id, boss) 
                          VALUES (?,?,?)''',
                       (user_name, tg_id, boss))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(user_id)))
        cursor.close()
        self.connection.commit()
