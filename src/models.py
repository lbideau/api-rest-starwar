from flask_sqlalchemy import SQLAlchemy
import os
import sys

db = SQLAlchemy()

""" class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        } """

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), unique=False, nullable=False)
    #favorite_id = db.Column(db.Integer, db.ForeignKey('favorite.id'))
    favorites  = db.relationship('Favorite', backref='user', uselist=True)
    def verifyLogin(self):
        """verify login"""
        pass
    def addToFavorite(self):
        """Add to Favorite """
        pass
    def removeFavorite(self):
        """remove Favorite"""
        pass

    def serialize(self):
        return {
            "user_name": self.user_name,
            "id": self.id
        }
    
    @classmethod
    def create(cls, bubulala):
        try:
            new_user = cls(**bubulala)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as error:
            db.session.rollback()
            print(error)
            return None

    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    url = db.Column(db.String(125), nullable=False) 
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint(
        'user_id',
        'url',
        name='unique_fav_for_user'
    ),)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "swapi_url": self.url,
            "url": "/detail/"+self.url.replace("https://www.swapi.tech/api/", ""),
            "id": self.id,
            "favName": self.name
        }
    
    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False
    # character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    # Vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    # planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    birth_day = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    skin_color = db.Column(db.String(80), nullable=False)

# class Vehicle(db.Model):
#     __tablename__ = 'vehicle'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False, unique=True)
#     crew = db.Column(db.String(80), nullable=False)
#     passenger = db.Column(db.String(80), nullable=False)
#     vehicle_class = db.Column(db.String(80), nullable=False)
#     model = db.Column(db.String(80), nullable=False)
#     manufacturer = db.Column(db.String(80), nullable=False)

# class Planet(db.Model):
#     __tablename__ = 'planet'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False, unique=True)
#     climate = db.Column(db.String(80), nullable=False)
#     terrain = db.Column(db.String(80), nullable=False)
#     gravity = db.Column(db.String (80), nullable=False) 
#     diameter = db.Column(db.Integer, nullable=False)
#     population = db.Column(db.Integer, nullable=False)  