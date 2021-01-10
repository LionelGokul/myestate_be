from models import Properties, PropertyImages, PropertyAmenities, PropertyRooms, PropertyRentPreferences, \
    PropertyFurnishings
from db import db
from Services.files import insertPropertyImage, removePropertyImage


def insertPropertyData(propertyDetails, propertyAmenities, propertyRooms, propertyRent, propertyFurnishings, files):
    propertyDetail = Properties(name=propertyDetails['name'], sqft=propertyDetails['area'],
                                city=propertyDetails['city'], latitude=propertyDetails['latitude'],
                                longitude=propertyDetails['longitude'], description=propertyDetails['description'],
                                price=propertyDetails['price'], bhk=propertyDetails['bhk'],
                                pincode=propertyDetails['pincode'], state="tamilnadu",
                                locality=propertyDetails['locality'],
                                street=propertyDetails['street'], type_id=propertyDetails['type'],
                                createdBy=propertyDetails['userId'])
    if propertyDetails['type'] != 1:
        propertyAemenity = PropertyAmenities(internet=propertyAmenities['internet'],
                                             carparking=propertyAmenities['carParking'],
                                             maintenance=propertyAmenities['maintenance'],
                                             rainWaterHarvesting=propertyAmenities['rainWaterHarvesting'],
                                             powerBackup=propertyAmenities['porwerBackup'],
                                             security=propertyAmenities['security'],
                                             park=propertyAmenities['park'], gym=propertyAmenities['gym'],
                                             lift=propertyAmenities['lift'],
                                             atm=propertyAmenities['atm'],
                                             reservedParking=propertyAmenities['reservedParking'],
                                             createdBy=propertyDetails['userId'],
                                             garden=propertyAmenities['garden'])
        db.session.add(propertyAemenity)
        db.session.flush()
        propertyDetail.amenities = propertyAemenity.id

        propertyRoom = PropertyRooms(bedRooms=propertyRooms['bedRooms'], washRooms=propertyRooms['washRooms'],
                                     balconies=propertyRooms['balconies'],
                                     halls=propertyRooms['halls'],
                                     createdBy=propertyDetails['userId'])
        db.session.add(propertyRoom)
        db.session.flush()
        propertyDetail.rooms = propertyRoom.id

        propertyfurnishing = PropertyFurnishings(bed=propertyFurnishings['bed'], ac=propertyFurnishings['ac'],
                                                 tv=propertyFurnishings['tv'],
                                                 diningTable=propertyFurnishings['diningTable'],
                                                 wifi=propertyFurnishings['wifiRouter'],
                                                 washingMachine=propertyFurnishings['washingMachine'],
                                                 createdBy=propertyDetails['userId'])
        db.session.add(propertyfurnishing)
        db.session.flush()
        propertyDetail.furnishings = propertyfurnishing.id

    if bool(propertyRent):
        propertyRent = PropertyRentPreferences(tenantType=propertyRent['tenantType'],
                                               work=propertyRent['tenantWork'],
                                               foodType=propertyRent['tenantFoodType'],
                                               minimumStay=propertyRent['tenantStay'],
                                               createdBy=propertyDetails['userId'])
        db.session.add(propertyRent)
        db.session.flush()
        propertyDetail.rentPreferences = propertyRent.id
    db.session.add(propertyDetail)
    db.session.flush()
    for file in files:
        images = PropertyImages(property_id=propertyDetail.id, createdBy=propertyDetails['userId'])
        url = insertPropertyImage(files[file], propertyDetail.id)
        if url:
            images.url = url
            db.session.add(images)
            db.session.flush()
        else:
            return
    db.session.commit()
    return True


def updatePropertyData(id, propertyDetails, propertyAmenities, propertyRooms, propertyRent, propertyFurnishings,
                       removedFiles, files):
    property = Properties.query.filter_by(id=id, isActive=True, isDeleted=False).first()
    Properties.query.filter_by(id=id, isActive=True, isDeleted=False).update(
        dict(name=propertyDetails['name'],
             sqft=propertyDetails['area'],
             city=propertyDetails['city'],
             latitude=propertyDetails[
                 'latitude'],
             longitude=propertyDetails[
                 'longitude'],
             description=propertyDetails[
                 'description'],
             price=propertyDetails['price'],
             bhk=propertyDetails['bhk'],
             pincode=propertyDetails[
                 'pincode'],
             state="tamilnadu",
             locality=propertyDetails[
                 'locality'],
             street=propertyDetails[
                 'street'],
             type_id=propertyDetails['type']))

    if property.rentPreferences is not None:
        PropertyRentPreferences.query.filter_by(id=property.rentPreferences, isActive=True, isDeleted=False).update(
            dict(
                tenantType=propertyRent['tenantType'],
                work=propertyRent['tenantWork'],
                foodType=propertyRent['tenantFoodType'],
                minimumStay=propertyRent['tenantStay'], ))

    if propertyDetails['type'] != 1:
        PropertyAmenities.query.filter_by(id=property.amenities, isActive=True, isDeleted=False).update(
            dict(
                internet=propertyAmenities['internet'],
                carparking=propertyAmenities['carParking'],
                maintenance=propertyAmenities['maintenance'],
                rainWaterHarvesting=propertyAmenities['rainWaterHarvesting'],
                powerBackup=propertyAmenities['porwerBackup'],
                security=propertyAmenities['security'],
                park=propertyAmenities['park'], gym=propertyAmenities['gym'],
                lift=propertyAmenities['lift'],
                atm=propertyAmenities['atm'],
                reservedParking=propertyAmenities['reservedParking'],
                garden=propertyAmenities['garden']))
        PropertyRooms.query.filter_by(id=property.rooms, isActive=True, isDeleted=False).update(
            dict(
                bedRooms=propertyRooms['bedRooms'], washRooms=propertyRooms['washRooms'],
                balconies=propertyRooms['balconies'],
                halls=propertyRooms['halls']))
        PropertyFurnishings.query.filter_by(id=property.furnishings, isActive=True, isDeleted=False).update(
            dict(
                bed=propertyFurnishings['bed'], ac=propertyFurnishings['ac'],
                tv=propertyFurnishings['tv'],
                diningTable=propertyFurnishings['diningTable'],
                wifi=propertyFurnishings['wifiRouter'],
                washingMachine=propertyFurnishings['washingMachine']))
    db.session.flush()

    for file in files:
        images = PropertyImages(property_id=property.id, createdBy=propertyDetails['userId'])
        url = insertPropertyImage(files[file], property.id)
        if url:
            images.url = url
            db.session.add(images)
            db.session.flush()
        else:
            return
    for removedFile in removedFiles:
        PropertyImages.query.filter_by(id=removedFile['id']).update(dict(isActive=False, isDeleted=True))
        removePropertyImage(PropertyImages.query.filter_by(id=removedFile['id']).first().url.split('/')[-1],
                            property.id)
        db.session.flush()
    db.session.commit()
    return True


def getPropertiesByUserId(userId):
    properties = Properties.query.filter_by(createdBy=userId).all()
    return [property.serialize for property in properties]


def getFeaturedProperties():
    properties = Properties.query.limit(8)
    return [property.serialize for property in properties]


def getPropertyDetailsById(id):
    property = Properties.query.filter_by(id=id).first()
    return property.serialize


def getCreatedBy(propertyId):
    return Properties.query.filter_by(id=propertyId, isActive=True, isDeleted=False).first().createdBy


def getPropertyDetailsByQuery(query):
    properties = Properties.query.filter(
        (Properties.name.ilike(f"{query}%") | Properties.city.ilike(f"{query}%")) | (Properties.pincode.ilike(f"{query}%")) | (
            Properties.locality.ilike(f"{query}%")))
    return [property.serialize for property in properties]


def getPropertiesDetailsByTypeId(typeId):
    properties = Properties.query.filter_by(type_id=typeId).all()
    return [property.serialize for property in properties]
