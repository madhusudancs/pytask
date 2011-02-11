#! /bin/bash
#
# Copyright 2011 Authors of PyTask.
#
# This file is part of PyTask.
#
# PyTask is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyTask is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyTask.  If not, see <http://www.gnu.org/licenses/>.
#
# authors__ = [
#     '"Madhusudan.C.S" <madhusudancs@fossee.in>',
#     ]


pg_dump pytask -U pytask -W > ~/pytaskdbdumps/dbdump`date +%Y%m%d%H%M%s`.dump
./bin/django dumpscript > ~/pytaskdbdumps/dbdumpscript`date +%Y%m%d%H%M%s`.dump
./bin/django dumpdata > ~/pytaskdbdumps/dbdumpdata`date +%Y%m%d%H%M%s`.dump
./bin/django schemamigration taskapp --auto
./bin/django migrate taskapp

