import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import setup_db, Movie, Actor
# from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)



@app.route('/actors')
def get_actors():
    # try:
      actors = Actor.query.order_by((Actor.id).all()
      if actors == []:
        abort(404)
      
      actors_format = [actor.format() for actor in actors]

      response = {
          "success": True,
          "actors": actors_format
      }
    # except:
    #     abort(404)

    return jsonify(response)

    

@app.route('/movies')
def get_movies():
    # try:
      movies = Movie.query.order_by((Movie.id).all()
      if movies == []:
        abort(404)
      
      movies_format = [movie.format() for movie in movies]

      response = {
          "success": True,
          "movies": movies_format
      }
    # except:
    #     abort(404)

    return jsonify(response)