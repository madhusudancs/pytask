#! /bin/bash

sudo -u postgres dropdb pytask
sudo -u postgres createdb -O pytask pytask
rm -r pytask/profile/migrations/
rm -r pytask/taskapp/migrations/
./bin/django schemamigration profile --initial
./bin/django schemamigration taskapp --initial
./bin/django syncdb
./bin/django migrate profile
./bin/django migrate taskapp
./bin/django loaddata sites_fixture.json 
./bin/django loaddata profile_fixture.json
