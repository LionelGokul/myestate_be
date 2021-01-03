from Controllers.Home import index
from Controllers.User import validateUser, createUser, updateUser
from Controllers.property import insertProperty, getPropertiesCreatedByUser, getPropertyDetails, updateProperty
from Controllers.Wishlist import addToWishlist, removeFromWishlist, getWishlistByUserId


def configure_URL(app):
    app.add_url_rule('/index', view_func=index, methods=['GET', 'POST'])
    app.add_url_rule('/users/login', view_func=validateUser, methods=['POST'])
    app.add_url_rule('/users', view_func=createUser, methods=['POST'])
    app.add_url_rule('/users/update', view_func=updateUser, methods=['POST'])
    app.add_url_rule('/properties', view_func=insertProperty, methods=['POST'])
    app.add_url_rule('/property/<id>', view_func=updateProperty, methods=['POST'])
    app.add_url_rule('/property/<id>', view_func=getPropertyDetails, methods=['GET'])
    app.add_url_rule('/wishlist', view_func=addToWishlist, methods=['POST'])
    app.add_url_rule('/removewishlist', view_func=removeFromWishlist, methods=['DELETE'])
    app.add_url_rule('/my-wishlist', view_func=getWishlistByUserId, methods=['POST'])
    app.add_url_rule('/my-properties', view_func=getPropertiesCreatedByUser, methods=['POST'])
