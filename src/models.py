from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "active": self.is_active,
            # do not serialize the password, its a security breach
        }
    

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    diameter = db.Column(db.String(50),unique=False, nullable=False)
    rotation_period = db.Column(db.String(50),unique=False, nullable=False)
    orbital_period = db.Column(db.String(50),unique=False, nullable=False)
    gravity = db.Column(db.String(50),unique=False, nullable=False)
    population = db.Column(db.String(50),unique=False, nullable=False)
    climate = db.Column(db.String(200), unique=False, nullable=False)
    terrain = db.Column(db.String(50),unique=False, nullable=False)
    surface_water = db.Column(db.String(50),unique=False, nullable=False)
    residents = db.Column(db.String(50),unique=False, nullable=False)
    films = db.Column(db.String(50),unique=False, nullable=False)
    url = db.Column(db.String(50),unique=False, nullable=False)
  

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "residents": self.residents,
            "films": self.films,
            "url": self.url,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    height = db.Column(db.String(50),unique=False, nullable=False)
    mass = db.Column(db.String(50),unique=False, nullable=False)
    hair_color = db.Column(db.String(50),unique=False, nullable=False)
    skin_color = db.Column(db.String(50),unique=False, nullable=False)
    eye_color = db.Column(db.String(50),unique=False, nullable=False)
    birth_year = db.Column(db.String(200), unique=False, nullable=False)
    gender = db.Column(db.String(50),unique=False, nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    films = db.Column(db.String(50),unique=False, nullable=False)
    url = db.Column(db.String(50),unique=False, nullable=False)
    planet = db.relationship(Planet)
  

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "planet_id": self.planet_id,
            "films": self.films,
            "url": self.url,
        }
    

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    user = db.relationship(User)
    planet = db.relationship(Planet)
    character = db.relationship(Character)

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,

        }

