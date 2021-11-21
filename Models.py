from datetime import datetime


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
                            WHERE id = ?''', (True, str(tg_id),))
        cursor.close()
        self.connection.commit()

    def insert(self, tg_id, user_name, boss=False):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (id, user_name, boss) 
                          VALUES (?,?,?)''',
                       (tg_id, user_name, boss, ))
        cursor.close()
        self.connection.commit()

    def get(self, tg_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(tg_id),))
        row = cursor.fetchone()
        if not row:
            return False
        return row

    def get_boss_id(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE boss = ?", (True,))
        row = cursor.fetchone()
        if not row:
            return False
        return row[0]

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def delete(self, tg_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(tg_id),))
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
                                     projects VARCHAR(200)
                                     )''')
        cursor.close()
        self.connection.commit()

    def auto_update(self):
        um = UserModel(self.connection)
        users = um.get_all()

        for u in users:
            if not u[2] and not self.get(u[0]):
                self.insert(u[0], u[1], '')

    def insert(self, tg_id, name, project_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO staff
                                  (id, name, projects) 
                                  VALUES (?,?,?)''',
                       (tg_id, name, project_id, ))
        cursor.close()
        self.connection.commit()

    def get(self, tg_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM staff WHERE id = ?", (str(tg_id), ))
        row = cursor.fetchone()
        if not row:
            return False
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM staff")
        rows = cursor.fetchall()
        return rows

    def get_id(self, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM staff WHERE name = ?", (name,))
        row = cursor.fetchone()
        if not row:
            return False
        return row[0]

    def get_by_project(self, project_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM staff WHERE project_id IN projects", (str(project_id), ))
        rows = cursor.fetchall()
        return rows

    def add_project(self, tg_id, project_id):
        projects = self.get(tg_id)[2]
        projects += str(project_id) + '-'

        cursor = self.connection.cursor()
        cursor.execute("UPDATE staff SET projects = ? WHERE id = ?", (projects, tg_id,))

    def del_project(self, tg_id, project_id):
        projects = self.get(tg_id)[2]
        projects = '-'.join([p for p in projects.split('-') if p != str(project_id)])

        cursor = self.connection.cursor()
        cursor.execute("UPDATE staff SET projects = ? WHERE id = ?", (projects, tg_id,))

    def delete(self, tg_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM staff WHERE id = ?''', (str(tg_id), ))
        cursor.close()
        self.connection.commit()


class TaskModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     name VARCHAR(256),
                                     description VARCHAR(4096),
                                     emp_id INTEGER,
                                     project_id INTEGER,
                                     done BOOL,
                                     done_date INTEGER,
                                     boss_link VARCHAR(100),
                                     timer VARCHAR(10)
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, description, emp_id, project_id, boss_link, timer, done=False, done_date=-1):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO tasks 
                                  (name, description, emp_id, project_id, done, done_date, boss_link, timer) 
                                  VALUES (?,?,?,?,?,?,?,?)''',
                       (name, description, emp_id, project_id, done, done_date, boss_link, timer))
        cursor.close()
        self.connection.commit()

    def get(self, tid):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (str(tid), ))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        return rows

    def delete(self, project_id, task_name):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM tasks WHERE project_id = ? AND name = ?''', (str(project_id), task_name, ))
        cursor.close()
        self.connection.commit()

    def delete_by_project(self, pid):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM tasks WHERE project_id = ?''', (str(pid),))
        cursor.close()
        self.connection.commit()

    def delete_by_emp(self, eid):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM tasks WHERE emp_id = ?''', (str(eid),))
        cursor.close()
        self.connection.commit()

    def get_by_project(self, project_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (str(project_id), ))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_by_emp(self, emp_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE emp_id = ?", (str(emp_id), ))
        rows = cursor.fetchall()
        return rows

    def search(self, name, project_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM tasks WHERE project_id = ? AND name = ?''', (project_id, name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return False

    def set_done(self, task_id, done=True):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE tasks SET 
                                done = ?
                                WHERE id = ?''', (done, task_id,))
        cursor.close()
        self.connection.commit()

    def set_done_date(self, task_id):
        date = datetime.toordinal(datetime.today())
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE tasks SET 
                                        done_date = ?
                                        WHERE id = ?''', (date, task_id,))
        cursor.close()
        self.connection.commit()

    def set_timer(self, task_id, timer):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE tasks SET 
                                        timer = ?
                                        WHERE id = ?''', (timer, task_id,))
        cursor.close()
        self.connection.commit()


class ProjectModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS projects
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     name VARCHAR(50)
                                     )''')
        cursor.close()
        self.connection.commit()

    def get_name(self, pid):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (str(pid), ))
        row = cursor.fetchone()
        if not row:
            return False
        return row[1]

    def get_id(self, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM projects WHERE name = ?", (name,))
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return False
        return row[0]

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

    def delete(self, pid):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM projects WHERE id = ?''', (str(pid),))
        cursor.close()
        self.connection.commit()


class ReportModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS reports
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     name VARCHAR(22),
                                     cad_num VARCHAR(17),
                                     address VARCHAR(4096),
                                     assignee VARCHAR(50),
                                     comment VARCHAR(4096),
                                     close_date DATE,
                                     client VARCHAR(50)
                                     )''')
        cursor.close()
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM reports")
        rows = cursor.fetchall()
        return rows

    def get(self, rid):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM reports WHERE id = ?''', (str(rid),))
        row = cursor.fetchone()
        return row

    def get_by_assignee(self, username):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM reports WHERE  assignee = ?''', (username,))
        row = cursor.fetchall()
        return row

    def insert(self, name, cad_num, address, client, assignee="", comment="", close_date="2222-01-01"):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO reports 
                                  (name, cad_num, address, assignee, comment, close_date, client) 
                                  VALUES (?,?,?,?,?,?,?)''',
                       (name, cad_num, address, assignee, comment, close_date, client))
        cursor.close()
        self.connection.commit()

    def set_assignee(self, rid, assignee):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE reports SET assignee = ? WHERE id = ?", (assignee, rid,))
        cursor.close()
        self.connection.commit()

    def close(self, rid, comment):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE reports SET comment = ? WHERE id = ?", (comment, rid,))
        cd = '-'.join((str(el) for el in datetime.timetuple(datetime.now())[:3]))
        cursor.execute("UPDATE reports SET close_date = ? WHERE id = ?", (cd, rid,))
        cursor.close()
        self.connection.commit()


    def delete(self, rid):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM reports WHERE id = ?''', (str(rid),))
        cursor.close()
        self.connection.commit()
