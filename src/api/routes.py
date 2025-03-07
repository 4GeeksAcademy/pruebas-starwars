"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users, Products, Bills, BillItems, Followers, Posts, Coments, Medias, Planets, PlanetFavourite, Characters, CharacterFavourites, Starships, StarshipFavourites
import requests
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

api = Blueprint('api', __name__)
CORS(api)  # Permitir solicitudes CORS

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {}
    response_body["message"] = "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    return jsonify(response_body), 200

@api.route('/users', methods=['GET'])
def users():
    response_body = {}
    rows = db.session.execute(db.select(Users)).scalars()  # Obtener todos los usuarios
    results = [row.serialize() for row in rows]  # Serializar cada usuario
    response_body["message"] = 'Listado de Usuarios'
    response_body["results"] = results
    return jsonify(response_body), 200

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@api.route("/login", methods=["POST"])
def login():
    response_body = {}
    data = request.json
    email = data.get("email", None)
    password = data.get("password", None)
    row = db.session.execute(db.select(Users).where(Users.email==email, Users.password==password, Users.is_active)).scalar()
    # Si la consulta es exitosa, row tendrá algo (por lo tanto es verdadero), si no devuelve None
    if not row:
        response_body['message'] = "Bad username or password"
        return response_body, 401
    access_token = create_access_token(identity=email)
    response_body['message'] = 'User logged!'
    response_body['access_token'] = access_token
    return response_body, 200

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    response_body = {}
    current_user = get_jwt_identity()
    response_body['message'] = f'User logged: {current_user}'
    return response_body, 200

@api.route('/products', methods=['GET', 'POST'])
def products():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(Products)).scalars()
        results = [row.serialize() for row in rows]
        response_body['results'] = results
        response_body['message'] = f'Respuesta para el metodo {request.method}'
        return jsonify(response_body), 200
    if request.method == 'POST':
        data = request.json
        row = Products(name=data['name'],
                       description=data.get('description', "n/a"),
                       price=data['price'])
        db.session.add(row)
        db.session.commit()
        response_body['message'] = f'Respuesta para el metodo {request.method}'
        response_body['results'] = row.serialize()
        return jsonify(response_body), 200

@api.route('/products/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def product(id):
    response_body = {}
    row = db.session.execute(db.select(Products).where(Products.id == id)).scalar()
    if not row:
        response_body['message'] = f'El producto id {id} no existe'
        return jsonify(response_body), 404

    if request.method == 'GET':
        response_body['result'] = row.serialize()
        response_body['message'] = f'Respuesta para el metodo {request.method} del id: {id}'
        return jsonify(response_body), 200
    if request.method == 'PUT':
        data = request.json
        row.name = data.get('name', row.name)
        row.description = data.get('description', row.description)
        row.price = data.get('price', row.price)
        db.session.commit()
        response_body['message'] = f'Respuesta para el metodo {request.method} del id: {id}'
        response_body['result'] = row.serialize()
        return jsonify(response_body), 200
    if request.method == 'DELETE':
        db.session.delete(row)
        db.session.commit()
        response_body['message'] = f'Se eliminó {request.method} del id: {id}'
        response_body['results'] = {}
        return jsonify(response_body), 200


#Quiero obtener todos los estudiantes de la cohorte 93
@api.route('/cohorts/<int:cohort_id>/students', methods=['GET'])
def cohortes_students(cohort_id):
    response_body = {}
    # logica para retornar esos datos
    return response_body, 200

@api.route('/jp-users', methods=['GET'])
def jp_users():
    response_body = {}
    url = 'https://jsonplaceholder.typicode.com/users'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        response_body['message'] = 'Listado de usaurios'
        response_body['resutls'] = data
        return response_body, 200
        response_body['message'] = 'Algo salió mal'
    return response_body, 400


@api.route('/jp-users/<int:id>', methods=['GET'])
def jp_users_id(id):
    response_body = {}
    url = f'https://jsonplaceholder.typicode.com/users/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        response_body['message'] = f'Este es el usuario con el id:{id}'
        response_body['resutls'] = data
        return response_body, 200
    response_body['message'] = 'Algo salió mal'
    return response_body, 400


@api.route('/characters', methods=['GET'])
def characters():
    response_body = {}
    url = 'https://swapi.tech/api/people'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        response_body['message'] = 'Listado de personajes'
        response_body['resutls'] = data['results']
        return response_body, 200
    response_body['message'] = 'Algo salió mal'
    return response_body, 400


@api.route('/characters/<int:id>', methods=['GET'])
def characters_id(id):
    response_body = {}
    url = f'https://swapi.tech/api/people/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        response_body['message'] = f'Este es el personaje con el id:{id}'
        response_body['resutls'] = data['result']['properties']
        return response_body, 200
    response_body['message'] = 'Algo salió mal'
    return response_body, 400

@api.route('/users/<int:user_id>/favorites-characters', methods=['GET'])
def get_favorite_characters(user_id):
    response_body = {}
    rows = db.session.execute(db.select(CharacterFavourites).where(CharacterFavourites.user_id == user_id)).scalars()
    results = [row.serialize() for row in rows]
    response_body['message'] = f'Listado de personajes favoritos del usuario {user_id}'
    response_body['results'] = results
    return jsonify(response_body), 200

@api.route('/users/<int:user_id>/favorite-characters', methods=['POST'])
def add_favorite_character(user_id):
    response_body = {}
    data = request.json
    character_id = data.get('character_id')
    row = CharacterFavourites(user_id=user_id, character_id=character_id)
    db.session.add(row)
    db.session.commit()
    response_body['message'] = f'Personaje {character_id} agregado a favoritos del usuario {user_id}'
    response_body['result'] = row.serialize()
    return jsonify(response_body), 200

@api.route('/users/<int:user_id>/favorite-characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    response_body = {}
    row = db.session.execute(db.select(CharacterFavourites).where(CharacterFavourites.user_id == user_id, CharacterFavourites.character_id == character_id)).scalar()
    if not row:
        response_body['message'] = f'El personaje {character_id} no está en favoritos del usuario {user_id}'
        return jsonify(response_body), 404
    db.session.delete(row)
    db.session.commit()
    response_body['message'] = f'Personaje {character_id} eliminado de favoritos del usuario {user_id}'
    return jsonify(response_body), 200

@api.route('/planets', methods=['GET'])
def planets():
    response_body = {}
    url = 'https://swapi.tech/api/planets'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        response_body['message'] = 'Listado de personajes'
        response_body['resutls'] = data['results']
        return response_body, 200
    response_body['message'] = 'Algo salió mal'
    return response_body, 400


@api.route('/planets/<int:id>', methods=['GET'])
def planets_id(id):
    response_body = {}
    url = f'https://swapi.tech/api/planets/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        response_body['message'] = f'Aqui el planeta con el id:{id}'
        response_body['resutls'] = data['result']['properties']
        return response_body, 200
    response_body['message'] = 'Algo salió mal'
    return response_body, 400


@api.route('/users/<int:user_id>/favorites-planets', methods=['GET'])
def get_favorite_planets(user_id):
    response_body = {}
    rows = db.session.execute(db.select(PlanetFavourite).where(PlanetFavourite.user_id == user_id)).scalars()
    results = [row.serialize() for row in rows]
    response_body['message'] = f'Listado de planetas favoritos del usuario {user_id}'
    response_body['results'] = results
    return jsonify(response_body), 200

@api.route('/users/<int:user_id>/favorite-planets', methods=['POST'])
def add_favorite_planet(user_id):
    response_body = {}
    data = request.json
    planet_id = data.get('planet_id')
    row = PlanetFavourite(user_id=user_id, planet_id=planet_id)
    db.session.add(row)
    db.session.commit()
    response_body['message'] = f'Planeta {planet_id} agregado a favoritos del usuario {user_id}'
    response_body['result'] = row.serialize()
    return jsonify(response_body), 200

@api.route('/users/<int:user_id>/favorite-planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    response_body = {}
    row = db.session.execute(db.select(PlanetFavourite).where(PlanetFavourite.user_id == user_id, PlanetFavourite.planet_id == planet_id)).scalar()
    if not row:
        response_body['message'] = f'El planeta {planet_id} no está en favoritos del usuario {user_id}'
        return jsonify(response_body), 404
    db.session.delete(row)
    db.session.commit()
    response_body['message'] = f'Planeta {planet_id} eliminado de favoritos del usuario {user_id}'
    return jsonify(response_body), 200

@api.route('/starships', methods=['GET'])
def starships():
    response_body = {}
    url = 'https://swapi.tech/api/starships'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        response_body['message'] = 'Listado de naves'
        response_body['resutls'] = data['results']
        return response_body, 200
    response_body['message'] = 'Algo salió mal'
    return response_body, 400

@api.route('/starships/<int:id>', methods=['GET'])
def starships_id(id):
    response_body = {}
    url = f'https://swapi.tech/api/starships/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        response_body['message'] = f'Esta es la nave con el id:{id}'
        response_body['resutls'] = data['result']['properties']
        return response_body, 200
    response_body['message'] = 'Algo salió mal'
    return response_body, 400