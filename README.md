# AUCR
[![Build Status](https://travis-ci.org/AUCR/AUCR.svg?branch=master)](https://travis-ci.org/AUCR/AUCR)
[![codecov](https://codecov.io/gh/AUCR/AUCR/branch/master/graph/badge.svg)](https://codecov.io/gh/AUCR/AUCR)
[![Docker Repository on Quay](https://quay.io/repository/wroersma/aucr/status "Docker Repository on Quay")](https://quay.io/repository/wroersma/aucr)
[![Coverage Status](https://coveralls.io/repos/github/AUCR/AUCR/badge.svg)](https://coveralls.io/github/AUCR/AUCR)
[![Code Health](https://landscape.io/github/AUCR/AUCR/master/landscape.svg?style=flat)](https://landscape.io/github/AUCR/AUCR/master)
[![AUCR Slack](https://slack.aucr.io/badge.svg)](https://slack.aucr.io/)


## Overview
Analyst Unknown Cyber Range is a micro services flask framework. The goal of this project to make highly scalable web services in a master framework so users have a single web interface to do all the things from. Think of what GCP/AWS is for admin users but for users(currently with a DFIR focus). 


## Developer setup
Example Setup with Temporary an example and just running with flask. If you use pycharm you can setup flask app to debug through the code. Python >= 3.6  

    pip install PyYAML
    pip install -r requiremnets.txt
    export FLASK_APP=aucr.py
    export FLASK_DEBUG=1
    flask run


## Easy Docker use
    sudo docker pull quay.io/wroersma/aucr
    sudo docker run aucr -p 5000:5000