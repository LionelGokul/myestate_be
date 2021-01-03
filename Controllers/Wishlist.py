import json
from flask import request
from Repositories.WishlistRepository import insertWishlistItems, removeFromWishlistByUserId, getWishlistsByUserId


def addToWishlist():
    data = request.get_json()
    try:
        wishlist = insertWishlistItems(data["userId"], data["propertyId"])
        print(wishlist)
        return json.dumps(wishlist), 200
    except Exception as e:
        return json.dumps(e), 500


def removeFromWishlist():
    data = request.get_json()
    try:
        wishlist = removeFromWishlistByUserId(data["userId"], data["propertyId"])
        print(wishlist)
        return json.dumps(wishlist), 200
    except Exception as e:
        return json.dumps(e), 500


def getWishlistByUserId():
    data = request.get_json()
    try:
        wishlist = getWishlistsByUserId(data['userId'])
        return json.dumps(wishlist), 200
    except Exception as e:
        return json.dumps(e), 500
