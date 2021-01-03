import os
from werkzeug.utils import secure_filename

IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
IMAGES_UPLOAD_FOLDER = 'static/images/'
API_URL = 'http://127.0.0.1:5000/'


def validateFile(fileName, extensions):
    return '.' in fileName and \
           fileName.rsplit('.', 1)[1].lower() in extensions


def insertImage(image):
    if validateFile(image.filename, IMAGE_EXTENSIONS):
        filename = secure_filename(image.filename)
        image.save(os.path.join(IMAGES_UPLOAD_FOLDER, filename))
        return API_URL + IMAGES_UPLOAD_FOLDER + filename
    return False


def insertPropertyImage(image, propertyId):
    if validateFile(image.filename, IMAGE_EXTENSIONS):
        filename = secure_filename(image.filename)
        os.makedirs(IMAGES_UPLOAD_FOLDER + str(propertyId), exist_ok=True)
        image.save(os.path.join(IMAGES_UPLOAD_FOLDER + str(propertyId), filename))
        return API_URL + IMAGES_UPLOAD_FOLDER + str(propertyId) + '/' + filename
    return False
