"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Starships
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required,JWTManager

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

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#       !!--USER--!!
@app.route('/user', methods=['GET'])
def handle_user():
   

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#       !!--LOGIN--!!
@app.route('/login', methods=['POST'])
def handle_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({
            "msg": "No account was found. Please check the email used or create an account."
        }), 401
    
    if password != user.password:
        return jsonify({"msg": "Incorrect password. Please try again."}), 401

    access_token = create_access_token(identity=email)

    payload = {"token":access_token, "msg": "Login successful"}
    return jsonify(payload), 200

#       !!--SIGN-UP--!!
@app.route('/signup', methods=['POST'])
def handle_signup():
    body = request.json # get the request body content
    email = request.json.get('email')
    name = request.json.get('name')

    password = request.json.get('password')
    
    if body is None:
        return "The request body is null", 400
    if not email:
        return 'You need to enter an email',400
    if not name:
        return 'You need to enter an name',400
    if not password:
        return 'You need to enter a password', 400
    check_user = User.query.filter_by(email=email).first()

    if check_user is not None:
        return jsonify({
            'msg': 'The email address already exists. Please login to your account to continue.'
        }),409

    user = User(email=email, name=name, password=password, is_active=True)

    db.session.add(user)
    db.session.commit()
   
    payload = {
        'msg': 'Your account has been registered successfully.',
        'user': user.serialize()
    }

    return jsonify(payload), 200

# get all characters
@app.route('/characters', methods=['GET'])
def getAllCharacters():
  characters = Characters.query.all()
  if characters is None:
    return jsonify(msg="This page does not exist")
  else:
    return jsonify(data=[character.serialize() for character in characters]) 

# get one Character
@app.route('/characters/<int:id>', methods=['GET'])
def getOneCharacters(id):
  character = Characters.query.get(id)
  if character is None:
    return jsonify(msg="This page does not exist")
  else:
    return jsonify(data=character.serialize())

# get all planets
@app.route('/planets', methods=['GET'])
def getAllPlanets():
  planets = Planets.query.all()
  if planets is None:
    return jsonify(msg="This page does not exist")
  else:
    return jsonify(data=[planet.serialize() for planet in planets]) 

# get one planet
@app.route('/planets/<int:id>', methods=['GET'])
def getOnePlanet(id):
  planet = Planets.query.get(id)
  if planet is None:
    return jsonify(msg="This page does not exist")
  else:
    return jsonify(data=planet.serialize())

# get all starships
@app.route('/starships', methods=['GET'])
def getAllStarships():
  starships = Starships.query.all()
  if starships is None:
    return jsonify(msg="This page does not exist")
  else:
    return jsonify(data=[starship.serialize() for starship in starships]) 

# get one starship
@app.route('/starships/<int:id>', methods=['GET'])
def getOneStarships(id):
  starship = Starship.query.get(id)
  if starship is None:
    return jsonify(msg="This page does not exist")
  else:
    return jsonify(data=starship.serialize())


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)