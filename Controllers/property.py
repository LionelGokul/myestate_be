from flask import request
import json
from Repositories.propertyRepository import insertPropertyData, getPropertiesByUserId, getPropertyDetailsById, updatePropertyData, getCreatedBy,getPropertyDetailsByQuery


def insertProperty():
    try:
        res = insertPropertyData(json.loads(request.form['propertyDetails']),
                                 json.loads(request.form['propertyAmenities']),
                                 json.loads(request.form['propertyRooms']),
                                 json.loads(request.form['propertyRent']),
                                 json.loads(request.form['propertyFurnishings']),
                                 request.files)
        return json.dumps(res), 200
    except Exception as e:
        return json.dumps(e), 500


def updateProperty(id):
    try:
        propertyDetails = json.loads(request.form['propertyDetails'])
        if getCreatedBy(id) == propertyDetails['userId']:
            print('updating')
            res = updatePropertyData(id,
                                     propertyDetails,
                                     json.loads(request.form['propertyAmenities']),
                                     json.loads(request.form['propertyRooms']),
                                     json.loads(request.form['propertyRent']),
                                     json.loads(request.form['propertyFurnishings']),
                                     json.loads(request.form['removedImages']),
                                     request.files)
            return 'success', 200
        return 'UnAuthorized User', 401
    except Exception as e:
        return json.dumps(e), 500


def getPropertiesCreatedByUser():
    try:
        reqData = request.get_json()
        res = getPropertiesByUserId(reqData['userId'])
        return json.dumps(res), 200
    except Exception as e:
        return json.dumps(e), 500


def getPropertyDetails(id):
    try:
        print(id)
        res = getPropertyDetailsById(id)
        return json.dumps(res), 200
    except Exception as e:
        return json.dumps(e), 500


def getProperties(query):
    try:
        print(query)
        res=getPropertyDetailsByQuery(query)
        return json.dumps(res),200
    except Exception as e:
        return json.dumps(e), 500