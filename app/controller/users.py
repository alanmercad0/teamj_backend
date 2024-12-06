from flask import jsonify
from app.dao.users import userDAO

class userController:

    def getAllUsers(self):
        dao = userDAO()
        result_tuples = dao.getAllUsers()
        result = []

        for row in result_tuples:
            result.append(row)
        return jsonify(result)
     
    def signup(self, json):
        if json:
            firstname = json['firstname']
            lastname = json['lastname']
            username = json['username']
            email = json['email']
            dob = json['dob']
            password = json['password']
            type = json['type']
            if firstname and lastname and username and dob and password and type and email:
                dao = userDAO()
                uid = dao.signup(firstname, lastname, username, email, dob, password, type)
                if(uid == 0):
                    return jsonify(Error="Username already in use. Try adding a number to your username or changing it."), 406
                result = {}
                result["firstname"] = firstname
                result["lastname"] = lastname
                result["username"] = username
                result['email'] = email
                result["dob"] = dob
                result["password"] = password
                result["type"] = type
                return jsonify(Users=result), 201
            else:
                return jsonify(Error="Malformed post request"), 400
        else:
            return jsonify(Error="Malformed post request"), 400
        
    def login(self, json):
        if json:
            username = json['username']
            password = json['password']

            if username and password:
                dao = userDAO()
                result_tuples = dao.login(username, password)
                result = []

                if (len(result_tuples) < 1):
                    return jsonify(Error="Submitted invalid Username or Password"), 401

                # for row in result_tuples:
                #     dict = self.build_login_dict(row)
                #     result.append(dict)
                return jsonify(result_tuples)
            else:
                return jsonify(Error="Malformed post request"), 400
        else:
            return jsonify(Error="Malformed post request"), 400
        
    def addToHistory(self, json):
        if json:
            uid = json["uid"]
            song_id = json["song_id"]

            if uid and song_id:
                dao = userDAO()
                newId = dao.addToHistory(uid, song_id)
                return jsonify(success="Successfully added to history")
            
    def getHistory(self, id):
        dao = userDAO()
        result_tuples = dao.getHistory(id)
        result = []
        for row in result_tuples:
            item = {}
            item['id'] = row[0]
            item['datetime'] = row[1]
            item['artist'] = row[2]
            item['title'] = row[3]
            item['genre'] = row[4] 
            item['liked'] = row[5]
            result.append(item)
        return jsonify(result)
    
    def getLikedSongs(self, id):
        dao = userDAO()
        result_tuples = dao.getLikedSongs(id)
        result = []
        for row in result_tuples:
            item = {}
            item['id'] = row[0]
            item['artist'] = row[1]
            item['title'] = row[2]
            item['genre'] = row[3] 
            result.append(item)
        return jsonify(result)
    
    def likeSong(self, json):
        if json:
            dao = userDAO()
            uid = json["uid"]
            song_id = json["song_id"]
            check = dao.checkIfLiked(uid, song_id)
            if check is None and uid and song_id:
                newId = dao.likeSong(uid, song_id)
                return jsonify(success="Successfully liked song"), 200
            elif check is not None:
                return jsonify(error='already added to liked songs'), 400
            
    def dislikeSong(self, json):
        if json:
            dao = userDAO()
            uid = json["uid"]
            song_id = json["song_id"]
            check = dao.checkIfLiked(uid, song_id)
            if check is None and uid and song_id:
                return jsonify(error='Song has not been liked'), 400
            elif check is not None:
                newId = dao.dislikeSong(uid, song_id)
                return jsonify(success="Successfully disliked song"), 200
            
    def checkIfLiked(self, uid, song_id):
        dao = userDAO()
        check = dao.checkIfLiked(uid, song_id)
        return jsonify(check)