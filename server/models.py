from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # A Camper has many Signups, -> camper.signups????
    signups = db.relationship('Signup', backref='camper')

    # A camper has many ActivityS through Signups -> camper.activities??????
    activities = association_proxy('signups', 'activity')

    # 
    serialize_rules = ("-signups.camper", '-signups.activity',    # many-to-one
                       "-activities.campers",                     # many-to-many
                       '-created_at', '-updated_at',)

    # serialize_rules = ('-activities.campers', -signups.activity')

    # Add validations to the Camper model:
    @validates("name", "age")
    def validate_name_age(self, key, string):
        # must have a name
        if string == "name":
            if not string:
                raise ValueError("Must have a name")
        # must have an age between 8 and 18
        elif string == "age":
            if not 8 <= string <= 18:
                raise ValueError('Age must be between 8 and 18.')
        return string


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # An Activity has many Signups, -> activity.signups
    signups = db.relationship('Signup', backref="activity")

    # An Activity has many Campers through Signups -> activity.campers
    campers = association_proxy("signups", "camper")

    # still have signups, but no signups.activity/ignups.camper
    # can set rules in to_dict(rules=('-signups',)) -> will not show signups
    serialize_rules = ("-signups.activity", "-signups.camper", # many-to-one
                       '-campers.activities', )                # many-to-many


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'
   
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    # A Signup belongs to a Camper and belongs to a Activity ???
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))

    # signup has 1 camper and one activity, so -camper.activities' and -activity.campers
    serialize_rules = ('-camper.activities', '-activity.campers', # many-many
                        "-camper.signups", "-activity.signups",   # one-many
                      )  


    @validates("time")
    def validate_time(self, key, time):
        if time < 0 and time > 23:
            raise ValueError("must have a time between 0 and 23 (referring to the hour of day for the activity)")
        return time