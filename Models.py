class UserModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY, 
                             user_name VARCHAR(50),
                             boss BOOL
                             )''')
        cursor.close()
        self.connection.commit()

    def make_boss(self, tg_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users SET 
                            boss = ?
                            WHERE id = ?''', (True, str(tg_id)))
        cursor.close()
        self.connection.commit()

    def insert(self, tg_id, user_name, boss=False):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (tg_id, user_name, boss) 
                          VALUES (?,?,?)''',
                       (tg_id, user_name, boss))
        cursor.close()
        self.connection.commit()

    def get(self, tg_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(tg_id)))
        row = cursor.fetchone()
        if not row:
            return False
        return row

    def delete(self, tg_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(tg_id)))
        cursor.close()
        self.connection.commit()


class EmployeeModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS staff 
                                    (id INTEGER PRIMARY KEY, 
                                     name VARCHAR(50),
                                     project_id INTEGER
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, tg_id, name, project_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO staff
                                  (tg_id, name, project_id) 
                                  VALUES (?,?,?)''',
                       (tg_id, name, project_id))
        cursor.close()
        self.connection.commit()

    def get(self, tg_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM staff WHERE id = ?", (str(tg_id)))
        row = cursor.fetchone()
        return row

    def get_by_project(self, project_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM staff WHERE project_id = ?", (str(project_id)))
        rows = cursor.fetchall()
        return rows

    def delete(self, tg_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM staff WHERE id = ?''', (str(tg_id)))
        cursor.close()
        self.connection.commit()


class TaskModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     name VARCHAR(50),
                                     description VARCHAR(200),
                                     emp_id INTEGER,
                                     project_id INTEGER,
                                     done BOOL
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, description, emp_id, project_id, done=False):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO tasks 
                                  (name, description, emp_id, project_id, done) 
                                  VALUES (?,?,?,?,?)''',
                       (name, description, emp_id, project_id, done))
        cursor.close()
        self.connection.commit()

    def get(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (str(id)))
        row = cursor.fetchone()
        return row

    def delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM tasks WHERE id = ?''', (str(id)))
        cursor.close()
        self.connection.commit()

    def get_by_project(self, project_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (str(project_id)))
        rows = cursor.fetchall()
        return rows

    def get_by_emp(self, emp_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE emp_id = ?", (str(emp_id)))
        rows = cursor.fetchall()
        return rows

    def set_done(self, done, task_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE tasks SET 
                                done = ?
                                WHERE id = ?''', (done, task_id,))
        cursor.close()
        self.connection.commit()


class ProjectModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS projects
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     name VARCHAR(50),
                                     )''')
        cursor.close()
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM projects")
        rows = cursor.fetchall()
        return rows

    def insert(self, name):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO projects 
                                  (name) 
                                  VALUES (?)''',
                       (name,))
        cursor.close()
        self.connection.commit()

    def delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM projects WHERE id = ?''', (str(id)))
        cursor.close()
        self.connection.commit()

