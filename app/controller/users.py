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
     
     def registerUser(self, json):
        if json and len(json) == 5:
            firstname = json['firstname']
            lastname = json['lastname']
            username = json['username']
            # email = json['email']
            dob = json['dob']
            password = json['password']
            type = json['type']
            if firstname and lastname and dob and password and type:
                dao = userDAO()
                uid = dao.insertUser(firstname, lastname, username, dob, password, type)
                if(uid == 0):
                    return jsonify(Error="Username already in use. Try adding a number to your username or changing it."), 406
                result = {}
                result["firstname"] = firstname
                result["lastname"] = lastname
                result["username"] = username
                result["dob"] = dob
                result["password"] = password
                result["type"] = type
                return jsonify(Users=result), 201
            else:
                return jsonify(Error="Malformed post request"), 400
        else:
            return jsonify(Error="Malformed post request"), 400