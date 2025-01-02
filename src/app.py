"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#------------------------------------------------
#USUARIOS
#------------------------------------------------

#Traer todos los usuarios
@app.route('/user', methods = ['GET'])
def get_users():
    try:
        users = User.query.all()
        if len(users) < 1:
            return jsonify({"msg": "Not found"}),404
        serializaed_users = list(map(lambda x: x.serialize(), users))
        return serializaed_users, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error": str(e)}),500
    
#Traer un usuario
@app.route("/user/<int:user_id>", methods = ["GET"])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify ({"msg": f"user {user_id} not found"}),404
        
        serialized_user = user.serialized()
        return serialized_user, 200
    except Exception as e:
        return jsonify ({"msg":"Server error", "error": str(e)}),500   

#Crear un usuario
@app.route("/user", methods = ["POST"])
def create_user():
    try:
        body = json.loads(request.data)
        new_user = User(
            email = body["email"],
            password = body["password"],
            is_active = True
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg":"user creadeted successfully"}),200
    except Exception as e:
        return jsonify({"msg":"Server error","error": str(e)}),500

#------------------------------------------------
#PLANETAS
#------------------------------------------------

#Traer todos los planetas
@app.route('/planet', methods = ['GET'])
def get_planets():
    try:
        planets = Planet.query.all()
        if len(planets) < 1:
            return jsonify({"msg": "Not found"}),404
        serializaed_planets = list(map(lambda x: x.serialize(), planets))
        return serializaed_planets, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error": str(e)}),500
    
#Traer un planeta
@app.route("/planet/<int:planet_id>", methods = ["GET"])
def get_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if planet is None:
            return jsonify ({"msg": f"planet {planet_id} not found"}),404
        
        serialized_planet = planet.serialized()
        return serialized_planet, 200
    except Exception as e:
        return jsonify ({"msg":"Server error", "error": str(e)}),500   

#Crear un planeta
@app.route("/planet", methods = ["POST"])
def create_planet():
    try:
        body = json.loads(request.data)
        new_planet = Planet(

            name = body["name"],
            diameter = body["diameter"],
            rotation_period = body["rotation_period"],
            orbital_period = body["orbital_period"],
            gravity = body["gravity"],
            population = body["population"],
            climate = body["climate"],
            terrain = body["terrain"],
            surface_water = body["surface_water"],
            residents = body["residents"],
            films = body["films"],
            url = body["url"]
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify({"msg":"planet creadeted successfully"}),200
    except Exception as e:
        return jsonify({"msg":"Server error","error": str(e)}),500
    


#------------------------------------------------
#PERSONAJES
#------------------------------------------------

#Traer todos los personajes
@app.route('/character', methods = ['GET'])
def get_characters():
    try:
        characters = Character.query.all()
        if len(characters) < 1:
            return jsonify({"msg": "Not found"}),404
        serializaed_characters = list(map(lambda x: x.serialize(), characters))
        return serializaed_characters, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error": str(e)}),500
    
#Traer un personaje
@app.route("/character/<int:character_id>", methods = ["GET"])
def get_charactert(character_id):
    try:
        character = Character.query.get(character_id)
        if character is None:
            return jsonify ({"msg": f"character {character_id} not found"}),404
        
        serialized_character = character.serialized()
        return serialized_character, 200
    except Exception as e:
        return jsonify ({"msg":"Server error", "error": str(e)}),500   

#Crear un personaje
@app.route("/character", methods = ["POST"])
def create_character():
    try:
        body = json.loads(request.data)
        new_character = Character(

            name = body["name"],
            height = body["height"],
            mass = body["mass"],
            hair_color = body["hair_color"],
            skin_color = body["skin_color"],
            eye_color = body["eye_color"],
            birth_year = body["birth_year"],
            gender = body["gender"],
            planet_id = body["planet_id"],
            films = body["films"],
            url = body["url"]
        )
        db.session.add(new_character)
        db.session.commit()
        return jsonify({"msg":"character creadeted successfully"}),200
    except Exception as e:
        return jsonify({"msg":"Server error","error": str(e)}),500




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
