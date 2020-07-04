# Casting Agency Capstone Project 

This Casting Agency project is invested in creating a relationship between actors and the agency. It provides a backend to keep track of all the actors and every movie they are a part of. In addition it also provides a list of actors for each movie. 
Moreover, it provides the functionality of creating new movies and adding new actors to the team! 
There are different roles within this agency that includes Casting Assistants, Casting Directors and Executive Producers. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


## Database Setup
With Postgres running, run the following commands: 
createdb capstone
createdb capstone_test


## Running the server

From within the `capstones` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to app file to find the application. 

## Error Handling 

Errors in this API are returned as JSON objects. They are formatted as: 
{
    "success" : False,
    "error" : 400,
    "message" : "Bad Request"
}

This API handles errors of types: 
- 400: Bad Request
- 404: Page not found
- 405: Method not allowed
- 422: unproccessable
- 500: Internal Server Error
- AuthError: Gets errors due to authorization and display the error code and message (e.g. Forbiddin, token expired, etc)


## API Endpoints 

### GET "/actors" 

### POST "/actors"

### PATCH "/actors/<actor_id>"

### DELETE "/actors/<actor_id>"


### GET "/movies"

### POST "/movies"

### PATCH "/movies/<movie_id>"

### DELETE "/movies/<movie_id>"






# Casting Agency Specifications
## The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Models:
- Movies with attributes title and release date - - DONE 
- Actors with attributes name, age and gender - - DONE 
- Relation between Movies & Actors - - DONE 

## Endpoints:
- GET /actors and /movies - - DONE 
- DELETE /actors/ and /movies/ - - DONE 
- POST /actors and /movies - - DONE 
- PATCH /actors/ and /movies/ - - DONE 

## Roles: 
- Casting Assistant
    - Can view actors and movies
- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
- Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

## Tests: 
- One test for success behavior of each endpoint - - DONE 
- One test for error behavior of each endpoint - - DONE 
- At least two tests of RBAC for each role - - DONE

## Authorizations: 
- Add Auth to app.py - - DONE
- create auth.py - - DONE
- add auth to test_app.py - - DONE




## Others: 


## README update: 
- roles and permissions are clearly defined in the project README
- Heroku URL is provided in project README
- Motivation for project
- Project dependencies, local development and hosting instructions,
- Detailed instructions for scripts to install any project dependencies, and to run the development server.
- Documentation of API behavior and RBAC controls