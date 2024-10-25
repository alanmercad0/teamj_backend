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