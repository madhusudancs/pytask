#! /bin/bash

pg_dump pytask -U pytask -W > ~/pytaskdbdumps/dbdump`date +%Y%m%d`.dump
./bin/django dumpscript > ~/pytaskdbdumps/dbdumpscript`date +%Y%m%d`.dump
./bin/django dumpdata > ~/pytaskdbdumps/dbdumpdata`date +%Y%m%d`.dump
./bin/django schemamigration taskapp --auto
./bin/django migrate taskapp

