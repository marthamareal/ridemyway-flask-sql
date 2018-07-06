# RIDE MY WAY API WITH DATABASE

[![Build Status](https://travis-ci.org/marthamareal/RideMyWayApi-DataBase.svg?branch=feature)](https://travis-ci.org/marthamareal/RideMyWayApi-DataBase.svg?branch=feature)
[![Coverage Status](https://coveralls.io/repos/github/marthamareal/RideMyWayApi-DataBase/badge.svg?branch=feature)](https://coveralls.io/github/marthamareal/RideMyWayApi-DataBase?branch=feature)
[![Maintainability](https://api.codeclimate.com/v1/badges/5ce1725652eea508ea13/maintainability)](https://codeclimate.com/github/marthamareal/RideMyWayApi-DataBase/maintainability)

### Installations

create a virtual environment with (virtualenv yourEnv).

Activate the virtual environment. (source yourEnv/bin/activate)

Install [postgres](https://www.postgresql.org/)

install [Python](https://www.python.org/)

Install [Flask](http://flask.pocoo.org/docs/1.0/installation/)

Install requirements (pip freeze > requirements.txt)

### Configurations

Create a .env file in your project

inside that file, export your enviroment variables by adding these lines.

export HOST_NAME='host_name'

export DB_NAME='your db'

export USER_NAME='your user name'

export PASSWORD='your password'

export SECRET_KEY='your secret' for creating tokens

export SCHEMA_FILE='path to tables.sql file in the project'

export DROP_SCHEMA_FILE='path to drop_tables.sql file in the project'

export TEST_DB_NAME='your test database' for running tests

### Endpoints in the API

|REQUEST TYPE| URL | DESCRIPTION |
|------------|-----|-------------|
|POST| /auth/signup |Create user account|
|POST| /auth/login |Login users with email and password|
|POST| /auth/logout |Logs out logged in users|
|POST| /rides/create |Create ride offer|
|GET| /rides/<int:ride_id> |shows ride offer details|
|GET| /rides/|gets all available ride offers|
|PUT| /rides/update/<int:ride_id> |Updates ride offer|
|DELETE| /rides/delete/<int:ride_id>|Deletes ride offer|
|POST| /rides/requests/create/<int:ride_id> |Request to join ride|
|GET| /rides/requests/<int:ride_id> |Get all requests on particular ride|
|POST,PUT| /rides/requests/approve/<int:request_id> |Approve ride request|

## Deployment

install [flassger](https://pypi.org/project/flasgger/) for documenting the api

Application is deployed using Heroku.

checkout on [View App](https://ride-my-way-api-database.herokuapp.com)