from models import Users
from db import db
from Services.files import insertUserImage


def validateUserByEmail(email, password):
    user = Users.query.filter_by(email=email, isActive=True, isDeleted=False).first()
    if user.check_password(password):
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'profilePic': user.profilePicture,
        }
    return {}


def insertUser(email, password, name, mobile):
    anyUser = checkIfUserExistsByEmail(email)
    if anyUser:
        return {
            'userAlreadyExists': True,
        }
    user = Users(name=name, email=email, mobile=mobile)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'profilePic': user.profilePicture,
        'mobile' : user.mobile,
    }


def checkIfUserExistsByEmail(email):
    user = Users.query.filter_by(email=email, isActive=True, isDeleted=False).first()
    if user is not None:
        return user
    return False


def checkIfUserExistsByGoogleLogin(googleId):
    user = Users.query.filter_by(googleid=googleId, isActive=True, isDeleted=False).first()
    if user is not None:
        return user
    return False


def GoogleLogin(email, name, googleId, profilePic):
    anyUser = checkIfUserExistsByGoogleLogin(googleId)
    if anyUser:
        return {
            'id': anyUser.id,
            'name': anyUser.name,
            'email': anyUser.email,
            'profilePic': anyUser.profilePicture,
            'mobile': anyUser.mobile,
        }
    user = Users(name=name, email=email, googleid=googleId, profilePicture=profilePic)
    user.set_password('')
    db.session.add(user)
    db.session.commit()
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'profilePic': user.profilePicture,
        'mobile': user.mobile,
    }


def setUserPassword(userId, password):
    user = Users(id=userId).first()
    if user:
        user.set_password(password)
        db.session.commit()
        return True
    return False


def updateUserData(userData):
    user = Users.query.filter_by(id=userData['userId'], isActive=True, isDeleted=False).first()
    if user:
        user.name = user.name if userData['name'] is None else userData['name']
        user.email = user.email if userData['email'] is None else userData['email']
        user.mobile = user.mobile if userData['mobile'] is None else userData['mobile']
        # if saveImage is true we don't need to update the image
        if userData['saveImage'] == 'true':
            url = insertUserImage(userData['image'], user.id)
            if url:
                user.profilePicture = url
            else:
                user.profilePicture = None
    db.session.commit()
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'profilePic': user.profilePicture,
        'mobile': user.mobile,
    }
