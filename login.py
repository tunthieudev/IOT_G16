import mysql.connector

class User:
    def __init__(self, username, password, fullname, role):
        self.id = None
        self.username = username
        self.password = password
        self.fullname = fullname
        self.role = role


class UserDAO:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="admin", database="pthttm"
        )
        self.cursor = self.db.cursor()

    def login(self, username, password):
        query = "SELECT * FROM user WHERE username=%s and password=%s"
        self.cursor.execute(
            query,
            (
                username,
                password,
            ),
        )
        rs = self.cursor.fetchone()
        self.cursor.close()
        if rs:
            return User(rs[1], rs[2], rs[3], rs[4])

    def signup(self, user):
        try:
            query = "INSERT INTO user (username, password,fullname,role) VALUES (%s,%s,%s, %s)"
            self.cursor.execute(
                query,
                (
                    user.username,
                    user.password,
                    user.fullname,
                    "0",
                ),
            )
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False
