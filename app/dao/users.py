from app.config.db_config import dbconfig
import psycopg2
import datetime

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
    

    def addToHistory(self, uid, song_id):
        cursor = self.conn.cursor()
        query = "insert into user_history(user_id, song_id) values (%s,%s) returning history_id"
        cursor.execute(query, (uid, song_id))
        insertId = cursor.fetchone()
        self.conn.commit()
        return insertId
    
    def getHistory(self, uid):
        # print('dao',uid)
        cursor = self.conn.cursor()
        query = """select s.song_id, date_uploaded, artist, title, genre, 
                        EXISTS (
                            SELECT *
                            FROM liked_songs liked
                            WHERE liked.song_id = s.song_id and liked.user_id = %s
                        ) AS liked
                    from user_history as h, songs as s where h.song_id = s.song_id and h.user_id = %s
                    order by date_uploaded desc"""
        cursor.execute(query, (uid, uid))
        result = []
        for row in cursor:
            print('row',row)
            result.append(row)
        return result
    
    def getLikedSongs(self, uid):
        # print('dao',uid)
        cursor = self.conn.cursor()
        query = """select s.song_id, artist, title, genre
                    from liked_songs as l, songs as s where l.song_id = s.song_id and l.user_id = %s
                    order by artist, title"""
        cursor.execute(query, (uid, ))
        result = []
        for row in cursor:
            print('row',row)
            result.append(row)
        return result
    
    def checkIfLiked(self, uid, song_id):
        cursor = self.conn.cursor()
        query = "select * from liked_songs where user_id = %s and song_id = %s"
        cursor.execute(query, (uid, song_id))
        check = cursor.fetchone()
        return check
    
    def likeSong(self, uid, song_id):
        cursor = self.conn.cursor()
        query = "insert into liked_songs(user_id, song_id) values (%s,%s) returning user_id"
        cursor.execute(query, (uid, song_id))
        insertId = cursor.fetchone()
        self.conn.commit()
        return insertId
    
    def dislikeSong(self, uid, song_id):
        cursor = self.conn.cursor()
        query = "delete from liked_songs where user_id = %s and song_id = %s returning user_id"
        cursor.execute(query, (uid, song_id))
        insertId = cursor.fetchone()
        self.conn.commit()
        return insertId

    