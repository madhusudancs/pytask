#! /bin/bash

pg_dump pytask -U pytask -W > ~/pytaskdbdumps/dbdump`date +%Y%m%d%H%M%s`.dump
./bin/django dumpscript > ~/pytaskdbdumps/dbdumpscript`date +%Y%m%d%H%M%s`.dump
./bin/django dumpdata > ~/pytaskdbdumps/dbdumpdata`date +%Y%m%d%H%M%s`.dump
./bin/django schemamigration profile --auto
./bin/django migrate profile

