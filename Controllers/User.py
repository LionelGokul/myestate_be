from flask import request
import json
from Repositories.UserRepository import insertUser, validateUserByEmail, GoogleLogin, updateUserData
from Repositories.WishlistRepository import  getWishlistsByUserId


def validateUser():
    try:
        if 'googleId' in request.json:
            user = GoogleLogin(request.json['email'], request.json['name'], request.json['googleId'],
                               request.json['imageUrl'])
            user['favList'] = getWishlistsByUserId(user['id'])
            return json.dumps(user), 200
        user = validateUserByEmail(request.json['email'], request.json['password'])
        # if user not found returning 401 status
        if not user:
            return json.dumps(user), 401
        user['favList'] = getWishlistsByUserId(user['id'])
        return json.dumps(user), 200
    except Exception as e:
        return json.dumps(e), 500


def createUser():
    try:
        user = insertUser(request.json['email'], request.json['password'], request.json['name'], request.json['mobile'])
        user['favList'] = []
        return json.dumps(user), 200
    except Exception as e:
        return json.dumps(e), 500


def updateUser():
    try:
        userData = {
            'email':  request.form['email'] if 'email' in request.form else None,
            'mobile': request.form['mobile'] if 'mobile' in request.form else None,
            'image': request.files['image'] if 'image' in request.files else None,
            'name': request.form['name'] if 'name' in request.form else None,
            'saveImage': request.form['saveImage'] if 'saveImage' in request.form else None,
            'userId': request.form['userId'] if 'userId' in request.form else None,
        }
        user = updateUserData(userData)
        user['favList'] = getWishlistsByUserId(user['id'])
        return json.dumps(user), 200
    except Exception as e:
        return json.dumps(e), 500
