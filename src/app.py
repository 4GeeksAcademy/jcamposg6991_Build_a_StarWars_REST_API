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
from models import db, User, Planet, People, Favorite
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
@app.route('/users', methods = ['GET'])
def get_users():
    try:
        users = User.query.all()
        if len(users) < 1:
            return jsonify({"msg": "Not found"}),404
        serialized_users = list(map(lambda x: x.serialize(), users))
        return serialized_users, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error": str(e)}),500
    
#Traer un usuario
@app.route("/users/<int:user_id>", methods = ["GET"])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify ({"msg": f"user {user_id} not found"}),404
        
        serialized_user = user.serialize()
        return jsonify(serialized_user), 200
    except Exception as e:
        return jsonify ({"msg":"Server error", "error": str(e)}),500   

#Crear un usuario
@app.route("/users", methods = ["POST"])
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
@app.route('/planets', methods = ['GET'])
def get_planets():
    try:
        planets = Planet.query.all()
        if len(planets) < 1:
            return jsonify({"msg": "Not found"}),404
        serialized_planets = list(map(lambda x: x.serialize(), planets))
        return serialized_planets, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error": str(e)}),500
    
#Traer un planeta
@app.route("/planets/<int:planet_id>", methods = ["GET"])
def get_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if planet is None:
            return jsonify ({"msg": f"planet {planet_id} not found"}),404
        
        serialized_planet = planet.serialize()
        return jsonify(serialized_planet), 200
    except Exception as e:
        return jsonify ({"msg":"Server error", "error": str(e)}),500   

#Crear un planeta
@app.route("/planets", methods = ["POST"])
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
@app.route('/people', methods = ['GET'])
def get_people():
    try:
        people = People.query.all()
        if len(people) < 1:
            return jsonify({"msg": "Not found"}),404
        serialized_people = list(map(lambda x: x.serialize(), people))
        return serialized_people, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error": str(e)}),500
    
#Traer un personaje
@app.route("/people/<int:people_id>", methods = ["GET"])
def get_person(people_id):
    try:
        people = People.query.get(people_id)
        if people is None:
            return jsonify ({"msg": f"people {people_id} not found"}),404
        
        serialized_people = people.serialize()
        return jsonify(serialized_people), 200
    except Exception as e:
        return jsonify ({"msg":"Server error", "error": str(e)}),500   

#Crear un personaje
@app.route("/people", methods = ["POST"])
def create_people():
    try:
        body = json.loads(request.data)
        new_people = People(

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
        db.session.add(new_people)
        db.session.commit()
        return jsonify({"msg":"people creadeted successfully"}),200
    except Exception as e:
        return jsonify({"msg":"Server error","error": str(e)}),500



#------------------------------------------------
#FAVORITOS
#------------------------------------------------

#Traer todos los favoritos
@app.route('/favorites', methods = ['GET'])
def get_favorites():
    try:
        favorites = Favorite.query.all()
        if len(favorites) < 1:
            return jsonify({"msg": "Not found"}),404
        serialized_favorites = list(map(lambda x: x.serialize(), favorites))
        return serialized_favorites, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error": str(e)}),500
    
#Traer un favorito
@app.route("/favorites/<int:favorite_id>", methods = ["GET"])
def get_favorite(favorite_id):
    try:
        favorite = Favorite.query.get(favorite_id)
        if favorite is None:
            return jsonify ({"msg": f"favorite {favorite_id} not found"}),404
        
        serialized_favorite = favorite.serialized()
        return serialized_favorite, 200
    except Exception as e:
        return jsonify ({"msg":"Server error", "error": str(e)}),500   

#Crear un favorito
@app.route("/favorites", methods = ["POST"])
def create_favorite():
    try:
        body = json.loads(request.data)
        new_favorite = Favorite(
            user_id = body["user_id"],
            planet_id = body["planet_id"],
            people_id = body["people_id"],
        )
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"msg":"favorite creadeted successfully"}),200
    except Exception as e:
        return jsonify({"msg":"Server error","error": str(e)}),500

#Traer favoritos por user
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    try:
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        if not favorites:
            return jsonify({"msg": f"No favorites found for user {user_id}"}), 404

        serialized_favorites = [favorite.serialize() for favorite in favorites]
        return jsonify(serialized_favorites), 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500


#Crear un planeta favorito para un usuario
@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    try:
        body = request.json
        user_id = body.get("user_id")
        if not user_id:
            return jsonify({"msg": "User ID is required"}), 400

        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"msg": f"Planet with ID {planet_id} not found"}), 404

        new_favorite = Favorite(user_id=user_id, planet_id=planet_id)

        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"msg": f"Planet {planet_id} added to favorites for User {user_id}"})
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
