# AUCR
[![Build Status](https://travis-ci.org/AUCR/AUCR.svg?branch=master)](https://travis-ci.org/AUCR/AUCR)
[![codecov](https://codecov.io/gh/AUCR/AUCR/branch/master/graph/badge.svg)](https://codecov.io/gh/AUCR/AUCR)
[![Docker Repository on Quay](https://quay.io/repository/wroersma/aucr/status "Docker Repository on Quay")](https://quay.io/repository/wroersma/aucr)
[![Coverage Status](https://coveralls.io/repos/github/AUCR/AUCR/badge.svg)](https://coveralls.io/github/AUCR/AUCR)
[![Code Health](https://landscape.io/github/AUCR/AUCR/master/landscape.svg?style=flat)](https://landscape.io/github/AUCR/AUCR/master)

## Overview
Analyst Unknown Cyber Range is a micro services flask framework. 


## Developer setup
Just run the server.py in debug mode from pycharm for the best development environment. It will auto generate the database for you!

        serve.py 



Example Setup with Temporary an  example yara_plugin and just running with flask

    export FLASK_APP=aucr.py
    export FLASK_DEBUG=1
    flask db init
    flask db upgrade
    flask run


## Example API Usage
Example API calls to generate an auth token and using it to query data using http 0.9.2

    http --auth admin:admin POST http://localhost:8080/auth/tokens
    
    HTTP/1.0 200 OK
    Content-Length: 106
    Content-Type: application/json
    Date: Fri, 16 Mar 2018 08:35:12 GMT
    Server: Werkzeug/0.14.1 Python/3.6.4
    
    {
        "token": "tTa0fv4+7oUdEZQcw0HiBwzMbPoYJPXZK63WvKvboNhDB1GJ3f0OIl+3Lio3UAAf31+B1qtz+NZSc+4FI6vO/w=="
    }
    
    http GET http://localhost:8080/api/groups/1 "Authorization:Bearer tTa0fv4+7oUdEZQcw0HiBwzMbPoYJPXZK63WvKvboNhDB1GJ3f0OIl+3Lio3UAAf31+B1qtz+NZSc+4FI6vO/w=="
    HTTP/1.0 200 OK
    Content-Length: 112
    Content-Type: application/json
    Date: Fri, 16 Mar 2018 08:35:36 GMT
    Server: Werkzeug/0.14.1 Python/3.6.4
    
    {
        "group_name": "admin", 
        "id": 1, 
        "time_stamp": "2018-03-16T08:17:48.115041Z", 
        "username": "admin"
    }

