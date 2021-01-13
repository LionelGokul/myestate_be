from models import Wishlist, Properties, PropertyType, PropertyImages
from db import db
import json


def insertWishlistItems(user_id, property_id):
    wishlist = Wishlist(user_id=user_id, property_id=property_id)
    db.session.add(wishlist)
    db.session.commit()
    return {
        'id': wishlist.id,
        'user_id': user_id,
        'property_id': property_id
    }


def removeFromWishlistByUserId(user_id, property_id):
    print("repo", property_id)
    Wishlist.query.filter_by(property_id=property_id, user_id=user_id).delete()
    db.session.commit()
    return {
        'property_id': property_id
    }


def getWishlistsByUserId(user_id):
    wishlists = Wishlist.query.filter_by(user_id=user_id).all()
    return [wishlist.property.serialize for wishlist in wishlists]
