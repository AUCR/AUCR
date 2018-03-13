# AUCR
[![Build Status](https://travis-ci.org/AUCR/AUCR.svg?branch=master)](https://travis-ci.org/AUCR/AUCR)
[![codecov](https://codecov.io/gh/AUCR/AUCR/branch/master/graph/badge.svg)](https://codecov.io/gh/AUCR/AUCR)
[![Docker Repository on Quay](https://quay.io/repository/wroersma/aucr/status "Docker Repository on Quay")](https://quay.io/repository/wroersma/aucr)
[![Coverage Status](https://coveralls.io/repos/github/AUCR/AUCR/badge.svg?t=THBtvq)](https://coveralls.io/github/AUCR/AUCR)


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
    flask db migrate -m "users table"
    flask db upgrade
    flask db migrate -m "groups table"
    flask db upgrade
    flask db migrate -m "tasks table"
    flask db upgrade
    flask db migrate -m "yara_plugin table"
    flask db upgrade
    flask run
