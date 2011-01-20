#! /usr/bin/python

"""Module to fill database with the tasks supplied in CSV.
This module takes the directory containing the csv files as
argument and creates task for the data in each CSV file in
this directory.
"""

__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@gmail.com>'
  ]


import csv
import datetime
import os
import sys

from django.contrib.auth.models import User

from pytask.taskapp.models import Task


STATIC_DATA = {
  'created_by': User.objects.get(pk=1),
  'creation_datetime': datetime.datetime.now()
  }


def get_textbooks_from_csv(directory, file_name):
    """Return the list of the titles of tasks.

    Args:
        file: name of the CSV file from which tasks must be fetched.
    """

    file_absolute_name = os.path.join(directory, file_name)

    csv_obj = csv.reader(open(file_absolute_name))

    # Nifty trick to separate the file extension out and get the
    # remaining part of the filename to use this as the tag for
    # branches/departments
    branch_name = os.extsep.join(file_name.split(os.extsep)[:-1])

    textbooks = []
    for line in csv_obj:
        if len(line) == 2:
            sep = ' by '
        else:
            sep = ''

        textbooks.append({
          'title': sep.join(line),
          'desc': '(To be filled in by the Coordinator or the T/A.)',
          'tags_field': ', '. join(['Textbook', branch_name, line[1]]),
          'pynts': 10,
          })

    return textbooks

def seed_db(data):
    """Seeds the database when the data is passed as the argument

    Args:
        data: A dictionary containing the data to be seeded into the
              task model.
    """

    for task in data:
        task.update(STATIC_DATA)
        task_obj = Task(**task)
        task_obj.save()

def main():
    """Just a wrapper function to make call the functions that perform
    the action.
    """

    for dir in sys.argv[1:]:
        args = list(os.walk(dir))
        files = args[0][2]
        for file_name in files:
            tasks = get_textbooks_from_csv(args[0][0], file_name)
            seed_db(tasks)

if __name__ == '__main__':
    main()
