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
- Auth0 is set up and running All required configuration settings are included in a bash file which export:
    - The Auth0 Domain Name
    - The JWT code signing secret
    - The Auth0 Client ID

- Deployment
    - API is hosted live via Heroku
    - URL is provided in project README
    - API can be accessed by URL and requires authentication

## README update: 
- roles and permissions are clearly defined in the project README
- Heroku URL is provided in project README
- Motivation for project
- Project dependencies, local development and hosting instructions,
- Detailed instructions for scripts to install any project dependencies, and to run the development server.
- Documentation of API behavior and RBAC controls