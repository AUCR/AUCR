# AUCR
[![Build Status](https://travis-ci.org/AUCR/AUCR.svg?branch=master)](https://travis-ci.org/AUCR/AUCR)
[![codecov](https://codecov.io/gh/AUCR/AUCR/branch/master/graph/badge.svg)](https://codecov.io/gh/AUCR/AUCR)
[![Docker Repository on Quay](https://quay.io/repository/wroersma/aucr/status "Docker Repository on Quay")](https://quay.io/repository/wroersma/aucr)
[![Coverage Status](https://coveralls.io/repos/github/AUCR/AUCR/badge.svg)](https://coveralls.io/github/AUCR/AUCR)
[![Code Health](https://landscape.io/github/AUCR/AUCR/master/landscape.svg?style=flat)](https://landscape.io/github/AUCR/AUCR/master)
[![AUCR Slack](https://slack.aucr.io/badge.svg)](https://slack.aucr.io/)


## Overview

Analyst Unknown Cyber Range is a micro services flask framework. The goal of this project to make highly scalable web 
services in a master framework so users have a single web interface to do all the things from. Think of what GCP/AWS is
 for admin users but for users(currently with a DFIR focus). 

### Database support

- sqllite
- mysql
- postgres

## Developer setup

Example Setup with Temporary an example and just running with flask. If you use pycharm you can setup flask app to debug
 through the code. Python >= 3.6  

    pip install PyYAML
    pip install -r requiremnets.txt
    export FLASK_APP=aucr.py
    export FLASK_DEBUG=1
    flask run


## Easy Docker use

    sudo docker pull quay.io/wroersma/aucr
    sudo docker run aucr -p 5000:5000


## Environment Variables

Here is an example env variables the aucr flask app will need. I use aucr.local as my host for all systems but normally 
in a production environment. 

### Required Services

- RabbitMQ 
- Database

### Optional Services

- Elasticsearch
- Object Storage

Example: Environment Variables

        LC_ALL=C.UTF-8
        LANG=C.UTF-8
        RABBITMQ_SERVER=aucr.local
        RABBITMQ_PORT=5672
        RABBITMQ_USERNAME=username
        RABBITMQ_PASSWORD=password
        ELASTICSEARCH_URL=http://aucr.local:9200
        POSTS_PER_PAGE=5
        DATABASE_URL=postgresql://username:password@aucr.local:5432/aucr
        ZIP_PASSWORD=infected
        FILE_FOLDER=/opt/aucr/upload/
        SECRET_KEY=some_thing_very_random_like_L23noSDONFSD8324809nsdf
        MAIL_SERVER=smtp.gmail.com
        MAIL_PORT=587
        MAIL_USERNAME=some_user_name_@gmail.com
        MAIL_PASSWORD=some_api_app_password_for_account
        ALLOWED_EXTENSIONS=['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'exe', 'yar', 'zip', 'dll', 'rar', '']
        MONGO_URI=mongodb://aucr.local:27017/aucr
        PRIVACY_POLICY_URL=https://app.termly.io/document/privacy-policy/ccb75cb3-f03e-43b6-bd09-de3b8c9e4d48
        MAIL_USE_TLS=True
        ALLOWED_EMAIL_LIST=gmail.com
        APP_TITLE=AUCR
        SERVER_NAME=aucr.local:5000
        TMP_FILE_FOLDER=/tmp/