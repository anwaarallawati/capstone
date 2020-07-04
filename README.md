# Casting Agency Capstone Project 

## Motivation

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

### To run the server locally: 
From within the `capstones` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to app file to find the application. 

### To use the deployed application on Heroku 
The server is up and running on heroku, you can use it using the following URL: 
https://capstone-anwaar.herokuapp.com

## Error Handling 

Errors in this API are returned as JSON objects. They are formatted as: 
```
{
    "success" : False,
    "error" : 400,
    "message" : "Bad Request"
}
```

This API handles errors of types: 
- 400: Bad Request
- 404: Page not found
- 405: Method not allowed
- 422: unproccessable
- 500: Internal Server Error
- AuthError: Gets errors due to authorization and display the error code and message (e.g. Forbiddin, token expired, etc)

## Models:
- Movies with attributes title and release date 
- Actors with attributes name, age and gender 
- Relation between Movies & Actors (many to many: a movie has many actors & actors act in many movies)


## API Endpoints 
* All endpoints must pass payload with the relevant token for the authorization, to do so you need to pass your token as a variable using the following command replacing <your_token> with your generated token (for the purpose of testing this project the tokens are listed at the end of this file): 
`export token="<your_token>"`

### GET "/actors" 
* General 

    * Fetches all the actors 
    * Request Arguments: None
    * Returns a single object, actors, that contains a string value corresponding to a key id 

* Sample request : 
`curl https://capstone-anwaar.herokuapp.com/actors -H "Authorization: Bearer ${token}" | jq` 
* Sample response: 
```
{
    "actors": [
        {
            "age": 30,
            "gender": "F",
            "id": 1,
            "movies": [
                1
            ],
            "name": "Actor 1"
        }
    ],
    "success": true
}
```

### POST "/actors"

* General 
    * Creates a new record for an actor, passes the arguments as a JSON object  
    * Request Arguments: name, age and gender 
    * Returns a single object, the newly created actor 

* Sample request: `curl https://capstone-anwaar.herokuapp.com/actors -X POST -H "Authorization: Bearer ${token}" -H "Content-Type:application/json" -d '{"name":"Actor 1", "age":30, "gender":"F"}' | jq` 

* Sample response: 
```
{
  "actor": {
    "age": 30,
    "gender": "F",
    "id": 6,
    "movies": [],
    "name": "Actor 1"
  },
  "success": true
}
```

### PATCH "/actors/<actor_id>"

* General 
    * Updates an existing record for an actor, passes the arguments as a JSON object  
    * Request Arguments: name, age and gender (one or more)
    * Returns a single object, the updated actor 

* Sample request: `curl https://capstone-anwaar.herokuapp.com/actors/6 -X PATCH -H "Authorization: Bearer ${token}" -H "Content-Type:application/json" -d '{"name":"Actor 6"}' | jq` 

* Sample response: 
```
{
  "actor": {
    "age": 30,
    "gender": "F",
    "id": 6,
    "movies": [],
    "name": "Actor 6"
  },
  "success": true
}
```

### DELETE "/actors/<actor_id>"

* General 
    * Deletes an existing record for an actor, passes the arguments as a JSON object  
    * Request Arguments: None
    * Returns a single object, the id of deleted actor 

* Sample request: `curl https://capstone-anwaar.herokuapp.com/actors/6 -X DELETE -H "Authorization: Bearer ${token}" -H "Content-Type:application/json" | jq` 

* Sample response: 
```
{
  "actor": 6,
  "success": true
}
```

### GET "/movies"

* General 
    * Fetches all the movies 
    * Request Arguments: None
    * Returns a single object, movies, that contains a string value corresponding to a key id 

* Sample request : 
`curl https://capstone-anwaar.herokuapp.com/movies -H "Authorization: Bearer ${token}" | jq` 
* Sample response: 
```
{
  "movies": [
    {
      "actors": [
        1,
        2
      ],
      "id": 1,
      "release_date": "Sun, 01 Mar 2020 00:00:00 GMT",
      "title": "Movie 1"
    }
  ],
  "success": true
}
```

### POST "/movies"

* General 
    * Creates a new record for a movie, passes the arguments as a JSON object  
    * Request Arguments: title and release date 
    * Returns a single object, the newly created movie  

* Sample request: `curl https://capstone-anwaar.herokuapp.com/movies -X POST -H "Authorization: Bearer ${token}" -H "Content-Type:application/json" -d '{"title" : "Movie 1","release_date" : "2020-03-01"}' | jq` 

* Sample response: 
```
{
  "movie": {
    "actors": [],
    "id": 4,
    "release_date": "Sun, 01 Mar 2020 00:00:00 GMT",
    "title": "Movie 1"
  },
  "success": true
}
```

### PATCH "/movies/<movie_id>"

* General 
    * Updates an existing record for a movie, passes the arguments as a JSON object  
    * Request Arguments: title and release date (one or more)
    * Returns a single object, the updated movie 

* Sample request: `curl https://capstone-anwaar.herokuapp.com/movies/4 -X PATCH -H "Authorization: Bearer ${token}" -H "Content-Type:application/json" -d '{"title":"Movie 4"}' | jq` 

* Sample response: 
```
{
  "movie": {
    "actors": [],
    "id": 4,
    "release_date": "Sun, 01 Mar 2020 00:00:00 GMT",
    "title": "Movie 4"
  },
  "success": true
}
```

### DELETE "/movies/<movie_id>"

* General 
    * Deletes an existing record for a movie, passes the arguments as a JSON object  
    * Request Arguments: None
    * Returns a single object, the id of deleted movie 

* Sample request: `curl https://capstone-anwaar.herokuapp.com/movies/4 -X DELETE -H "Authorization: Bearer ${token}" -H "Content-Type:application/json" | jq` 

* Sample response: 
```
{
  "movie": 4,
  "success": true
}
```

## Authentication, Roles & Permissions
* This API uses Auth0 JWT tokens, for the purpose of testing the tokens are provided at the end of this files. These tokens are role-based. This project uses 3 roles mentioned below. 

- Casting Assistant
    - Can view actors and movies
- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
- Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database


## Testing
* The file test_app.py includes a series of unitest based tests for each endpoint in the API 
* It includes test cases with successful outcomes as well as unsuccessful ones 
* To run the tests, run the following commands 
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone_sql.psql
source setup.sh
python test_app.py
```


## TOKENS: 

### Executive Producer 
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5ODJkM2UwZGU4MDAxMzk3MDI3NiIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzkwMDYyMCwiZXhwIjoxNTkzOTg3MDIwLCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.WN0WJwAIm9ifiYX9BSguz9lHx5-cbv1U4QrJpFqek7wd0VxOH8NePyWyobKNxz5AXIY7A5C4ZtsG_PgBewnOanUPfC87GhnCfhAZ2vF6qXOA72F7bDj4resEApkZ1qftmFuBvL15wH79QPt3mKcpFAc21JhyngugHCi1Kw_Hgkj6SM1bMXVwLRGfa7D6bl27gUD9inX1_UJnYiSd_h723dU5wdHxQ8-GgeahWV-OxuGvhYBnbXfUbA7xuELi6JVFlw14UIrVld-WnXzUtsPKWsdit-3a1wOOp7CHDa5faEYFhvIwTXYqYt-ZDdKofANH6-wRqRsiYltYilRNvcnTrQ
```

### Casting Director 
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5ODBjZDQ0ZWQ4MDAxOTQ0NmZkYyIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzkwMDU4NiwiZXhwIjoxNTkzOTg2OTg2LCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.KY3oudlBsYVPA4FgXmr5W86DkVqZr93MkMpQpoQfWTY6tysnixDQOrO34-9VtWwdsxpMvbh43ZfgzqbB25iVsNGQwCIS404hSnVIPjpRC40LtZnnWwBO-wDHke1DuR0xeLwSJXeYLN0cCFrGV1gzO4ZfqzsUz2h11t_WXaM-qxrvgNH6fpNUIjGm2PD3qM8cIuE7Fn8MTvNbFiiu8VSl1eafowdaaGCfdqTu4ChNBmaIoCFIxT3ZZhwDuD9ByZKOsBsPPpxH4pr3S3I2Y3nO3Iuks4cwDC33LUhiY2DzYCfk1gx4aoWHFXpZ73BhBexGua_0ukTTzIv_wHjNOEeHQg
```

### Casting Assistant 
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5N2RmOTI4ODJjMDAxMzViOGU3MiIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzkwMDQ0NCwiZXhwIjoxNTkzOTg2ODQ0LCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.emZpeine11R-7JgFClbVoICGCD0bN_wltRNX5E4nnOFCdL1BSU_2Wetf1MJiMiBubZ2cQA0TuFXFpzB5F-XZpg5WRf0SKhNoabM_0uL9WgwYGPnznz6RO3tNP275BGqt1_UKbh_99oO1TasWw6dNs67fF1t8ET4wjQ3U27VxTBQuaho2viqXKBMGwF1pQ0_zwcPFWUtIeLnUIrk7DPfbfUsuVNuNsuWnVVBxTzj6nDLRrwAbElQJKY9nzynOMeEwRK3siWTrT5MN-gT7Qvqj1oYcAJ-d_GZRUW74bCG5DENZw_2P_kgY1vXQuVlJlIO7jTLik35LTpNhfHOEt1LmtQ
```

