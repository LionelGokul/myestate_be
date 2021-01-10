from Controllers.Home import index
from Controllers.User import validateUser, createUser, updateUser
from Controllers.property import insertProperty, getPropertiesCreatedByUser, getPropertyDetails, \
    updateProperty, getProperties, getPropertiesByType, featuredProperties
from Controllers.Wishlist import addToWishlist, removeFromWishlist, getWishlistByUserId
from Controllers.Feedback import feedback


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
    app.add_url_rule('/search/<query>', view_func=getProperties, methods=['GET'])
    app.add_url_rule('/feedback', view_func=feedback, methods=['POST'])
    app.add_url_rule('/properties/<type>', view_func=getPropertiesByType, methods=['GET'])
    app.add_url_rule('/featured', view_func=featuredProperties, methods=['GET'])
