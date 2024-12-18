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
from models import db, User
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


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
