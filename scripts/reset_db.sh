#! /bin/bash

sudo -u postgres dropdb pytask
sudo -u postgres createdb -O pytask pytask
./bin/django syncdb
./bin/django migrate profile
./bin/django migrate taskapp
./bin/django loaddata sites_fixture.json 

