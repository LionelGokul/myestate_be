from db import db
from werkzeug.security import generate_password_hash, check_password_hash

propertyTypeData = ['Land', 'Appartment', 'Villa', 'House']


# Model Users is parent to the Property Model
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    googleid = db.Column(db.String(100), default=None, nullable=True)
    facebookid = db.Column(db.String(100), default=None, nullable=True)
    email = db.Column(db.String(200), default=None, unique=True, nullable=False)
    mobile = db.Column(db.String(100), default=None, nullable=True)
    password = db.Column(db.String(150), nullable=True)
    profilePicture = db.Column(db.String(200), default=None, nullable=True)
    isActive = db.Column(db.Boolean, default=True)
    isDeleted = db.Column(db.Boolean, default=False)
    createdOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    updatedOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    properties = db.relationship("Properties", backref="users", lazy=True)

    # password hashing

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class PropertyType(db.Model):
    __tablename__ = "propertytype"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    createdOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    createdBy = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    isActive = db.Column(db.Boolean, default=True)
    isDeleted = db.Column(db.Boolean, default=False)
    # establish relationship with properties model with properties.id as f-key

    # props type to properties
    properties = db.relationship("Properties", backref="propertytype", uselist=False)


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    feedback = db.Column(db.String(1000), nullable=False)
    createdOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    createdBy = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    isActive = db.Column(db.Boolean, default=True)
    isDeleted = db.Column(db.Boolean, default=False)


@db.event.listens_for(PropertyType.__table__, "after_create")
def insertPropertyTypeValues(*args, **kwargs):
    for data in propertyTypeData:
        db.session.add(PropertyType(type=data))
    db.session.commit()


class Properties(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sqft = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    bhk = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(200), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    locality = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    # Foreign keys
    amenities = db.Column(db.Integer, db.ForeignKey("propertyamenities.id"), nullable=True)
    rentPreferences = db.Column(db.Integer, db.ForeignKey("propertyrentpreferences.id"), nullable=True)
    furnishings = db.Column(db.Integer, db.ForeignKey("propertyfurnishings.id"), nullable=True)
    rooms = db.Column(db.Integer, db.ForeignKey("propertyrooms.id"), nullable=True)

    propertyAmenities = db.relationship("PropertyAmenities", backref="Properties", lazy=True)
    propertyRentPreferences = db.relationship("PropertyRentPreferences", backref="Properties", lazy=True)
    propertyFurnishings = db.relationship("PropertyFurnishings", backref="Properties", lazy=True)
    propertyRooms = db.relationship("PropertyRooms", backref="Properties", lazy=True)

    createdOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    updatedOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    # establish relationship with my estate Users model with users.id as f-key
    createdBy = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    isDeleted = db.Column(db.Boolean, default=False)

    # properties to props type
    # properties = db.relationship("PropertyType", backref="properties", lazy=True)

    # properties to images
    type_id = db.Column(db.Integer, db.ForeignKey("propertytype.id"))
    # property to images
    images = db.relationship('PropertyImages', backref='properties', lazy=True)
    propertyType = db.relationship('PropertyType', backref='propertytype', lazy=True)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'sqft': self.sqft,
            'price': self.price,
            'bhk': self.bhk,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'description': self.description,
            'pincode': self.pincode,
            'city': self.city,
            'state': self.state,
            'street': self.street,
            'locality': self.locality,
            'propertyAmenities': None if self.propertyAmenities is None else self.propertyAmenities.serialize,
            'propertyRentPreferences': None if self.propertyRentPreferences is None else self.propertyRentPreferences.serialize,
            'propertyFurnishings': None if self.propertyFurnishings is None else self.propertyFurnishings.serialize,
            'propertyRooms': None if self.propertyRooms is None else self.propertyRooms.serialize,
            'createdOn': self.createdOn.isoformat(),
            'updatedOn': self.updatedOn.isoformat(),
            'propertyType': self.propertyType.type,
            'name': self.name,
            'images': self.serialize_many2many,
        }

    @property
    def serialize_many2many(self):
        images = []
        for item in self.images:
            if item.isActive and not item.isDeleted:
                images.append(item.serialize)
        return images


class PropertyImages(db.Model):
    __tablename__ = "propertyimages"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    url = db.Column(db.String(200), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'),
                            nullable=False)
    createdOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    createdBy = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    isDeleted = db.Column(db.Boolean, default=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'url': self.url,
            'createdOn': self.createdOn.isoformat(),
            'isActive': self.isActive,
            'isDeleted': self.isDeleted,
        }


class PropertyAmenities(db.Model):
    __tablename__ = "propertyamenities"
    id = db.Column(db.Integer, primary_key=True)
    carparking = db.Column(db.Boolean, default=False)
    internet = db.Column(db.Boolean, default=False)
    maintenance = db.Column(db.Boolean, default=False)
    rainWaterHarvesting = db.Column(db.Boolean, default=False)
    powerBackup = db.Column(db.Boolean, default=False)
    security = db.Column(db.Boolean, default=False)
    park = db.Column(db.Boolean, default=False)
    gym = db.Column(db.Boolean, default=False)
    garden = db.Column(db.Boolean, default=False)
    lift = db.Column(db.Boolean, default=False)
    atm = db.Column(db.Boolean, default=False)
    reservedParking = db.Column(db.Boolean, default=False)
    createdOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    updatedOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    createdBy = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    isDeleted = db.Column(db.Boolean, default=False)

    @property
    def serialize(self):
        return {
            'carparking': self.carparking,
            'internet': self.internet,
            'maintenance': self.maintenance,
            'rainWaterHarvesting': self.rainWaterHarvesting,
            'powerBackup': self.powerBackup,
            'security': self.security,
            'park': self.park,
            'gym': self.gym,
            'garden': self.garden,
            'lift': self.lift,
            'atm': self.atm,
            'reservedParking': self.reservedParking,
        }


class PropertyRooms(db.Model):
    __tablename__ = "propertyrooms"
    id = db.Column(db.Integer, primary_key=True)
    bedRooms = db.Column(db.Integer, nullable=False)
    washRooms = db.Column(db.Integer, nullable=False)
    balconies = db.Column(db.Integer, nullable=False)
    halls = db.Column(db.Integer, nullable=False)
    createdOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    updatedOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    createdBy = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    isDeleted = db.Column(db.Boolean, default=False)

    @property
    def serialize(self):
        return {
            'bedRooms': self.bedRooms,
            'washRooms': self.washRooms,
            'halls': self.halls,
            'balconies': self.balconies,
        }


class PropertyFurnishings(db.Model):
    __tablename__ = "propertyfurnishings"
    id = db.Column(db.Integer, primary_key=True)
    bed = db.Column(db.Integer, nullable=False)
    ac = db.Column(db.Integer, nullable=False)
    tv = db.Column(db.Integer, nullable=False)
    diningTable = db.Column(db.Boolean, default=False)
    wifi = db.Column(db.Boolean, default=False)
    washingMachine = db.Column(db.Boolean, default=False)
    createdOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    updatedOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    createdBy = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    isDeleted = db.Column(db.Boolean, default=False)

    @property
    def serialize(self):
        return {
            'bed': self.bed,
            'ac': self.ac,
            'tv': self.tv,
            'diningTable': self.diningTable,
            'wifi': self.wifi,
            'washingMachine': self.washingMachine,
        }


class PropertyRentPreferences(db.Model):
    __tablename__ = "propertyrentpreferences"
    id = db.Column(db.Integer, primary_key=True)
    tenantType = db.Column(db.String(50), nullable=False)
    work = db.Column(db.String(50), nullable=False)
    foodType = db.Column(db.String(50), nullable=False)
    minimumStay = db.Column(db.String(50), nullable=False)
    createdOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    updatedOn = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                          server_onupdate=db.func.current_timestamp())
    createdBy = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    isDeleted = db.Column(db.Boolean, default=False)

    @property
    def serialize(self):
        return {
            'tenantType': self.tenantType,
            'foodType': self.foodType,
            'minimumStay': self.minimumStay,
            'work': self.work
        }


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    property = db.relationship('Properties', backref='properties', lazy=True)
