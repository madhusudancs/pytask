#! /bin/bash

pg_dump pytask -U pytask -W > ~/dumps/dbdump`date +%Y%m%d`.dump
./bin/django dumpscript > ~/dumps/dbdumpscript`date +%Y%m%d`.dump
./bin/django dumpdata > ~/dumps/dbdumpdata`date +%Y%m%d`.dump

