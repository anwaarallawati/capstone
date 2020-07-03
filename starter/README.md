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

## Tests: (one remaining for RBAC)
- One test for success behavior of each endpoint - - DONE 
- One test for error behavior of each endpoint - - DONE 
- At least two tests of RBAC for each role - - 

## Authorizations: (one remaining for test.py)
- Add Auth to app.py - - DONE
- create auth.py - - DONE
- add auth to test_app.py

## Others: 
- update README file 