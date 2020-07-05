import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)
    CORS(app)

#---------------------------------------------
# Actor ENDPOINTS
#-----------------------------
# (1) GET Actors endpoint
#-----------------------------

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):

        actors = Actor.query.order_by(Actor.id).all()

        if actors is None:
            abort(404)

        try:
            actors_format = [actor.format() for actor in actors]

            response = {
                "success": True,
                "actors": actors_format
            }
        except BaseException:
            abort(404)

        return jsonify(response)

    #-----------------------------#
    # (2) DELETE Actors endpoint
    #-----------------------------#

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).first()

        if actor is None:
            abort(404)

        try:
            actor.delete()
            response = {
                "success": True,
                "actor": actor_id
            }
        except BaseException:
            abort(422)

        return jsonify(response)

    #-----------------------------#
    # (3) POST Actors endpoint
    #-----------------------------#

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        actor = Actor(
            name=name,
            age=age,
            gender=gender
        )

        try:
            actor.insert()

            response = {
                "success": True,
                "actor": actor.format()
            }
        except BaseException:
            abort(422)

        return jsonify(response)

    #-----------------------------#
    # (4) PATCH Actors endpoint
    #-----------------------------#

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actors(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).first()

        if actor is None:
            abort(404)

        body = request.get_json()

        if 'name' in body:
            actor.name = body.get('name', None)
        if 'age' in body:
            actor.age = body.get('age', None)
        if 'gender' in body:
            actor.gender = body.get('gender', None)

        try:
            actor.update()
            actor_new = Actor.query.filter(Actor.id == actor_id).first()
            response = {
                "success": True,
                "actor": actor_new.format()
            }
        except BaseException:
            abort(422)

        return jsonify(response)

    #------------------------------------------------------------------------------------------#

    # Movies ENDPOINTS
    #-----------------------------#
    # (1) GET Movies endpoint
    #-----------------------------#

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):

        movies = Movie.query.order_by(Movie.id).all()

        if movies is None:
            abort(404)
        try:
            movies_format = [movie.format() for movie in movies]

            response = {
                "success": True,
                "movies": movies_format
            }
        except BaseException:
            abort(404)

        return jsonify(response)

    #-----------------------------#
    # (2) DELETE Movies endpoint
    #-----------------------------#

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).first()

        if movie is None:
            abort(404)

        try:
            movie.delete()
            # movies_all = Movie.query.order_by((Movie.id).all()
            # movies_format = [movie.format() for movie in movies]
            response = {
                "success": True,
                "movie": movie_id
            }
        except BaseException:
            abort(422)

        return jsonify(response)

    #-----------------------------#
    # (3) POST Movies endpoint
    #-----------------------------#

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(payload):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        movie = Movie(
            title=title,
            release_date=release_date
        )

        try:
            movie.insert()

            response = {
                "success": True,
                "movie": movie.format()
            }
        except BaseException:
            abort(422)

        return jsonify(response)

    #-----------------------------#
    # (4) PATCH Movies endpoint
    #-----------------------------#

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).first()

        if movie is None:
            abort(404)

        body = request.get_json()
        if 'title' in body:
            movie.title = body.get('title', None)
        if 'release_date' in body:
            movie.release_date = body.get('release_date', None)

        try:
            movie.update()
            movie_new = Movie.query.filter(Movie.id == movie_id).first()
            response = {
                "success": True,
                "movie": movie_new.format()
            }
        except BaseException:
            abort(422)

        return jsonify(response)

    #-----------------------------#
    # (*) Error Handlers
    #-----------------------------#

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Page not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(422)
    def unproccessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unproccessable"
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method_not_allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": " Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    #------------------------------------------------------------------------------------------#

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
