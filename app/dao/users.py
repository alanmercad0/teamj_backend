from app.config.db_config import dbconfig
import psycopg2

class userDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s " \
                         % (dbconfig['dbname'], dbconfig['user'], dbconfig['password'], dbconfig['dbhost'],
                            dbconfig['dbport'])

        self.conn = psycopg2.connect(connection_url)

    def getAllUsers(self):
        query = "select * from users"
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    

    def signup(self, firstname, lastname, username, email, dob, password, type):
        cursor = self.conn.cursor()
        query = "insert into users(first_name, last_name, username, email, dob, password, type) values (%s, %s, %s, %s, %s, %s, %s) on conflict do nothing returning user_id;"
        cursor.execute(query, (firstname, lastname, username, email, dob, password, type))

        uidfetch = cursor.fetchone()
        if uidfetch is None:
            uid = 0;
        else:
            uid = uidfetch[0]
        self.conn.commit()
        return uid
    
    def login(self, username, password):
        cursor = self.conn.cursor()
        query = "select * from users where username = %s and password = %s"
        cursor.execute(query, (username, password))
        getResult = []
        for row in cursor:
            getResult.append(row)
        return getResult
    