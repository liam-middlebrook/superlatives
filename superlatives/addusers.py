from database import init_db

from flask import Flask, jsonify
import json
import sys

json_config = None

#connect to db

with open(sys.argv[1]) as config_file:
    json_config = json.load(config_file)

    init_db(json_config['db']['url'])

import models
from database import db_session

# populate users

with open(sys.argv[2]) as people_file:
    for line in people_file:
        line = line.rstrip('\n').split(',')
        db_session.add(models.Person(line[0], line[1]))

db_session.flush()
db_session.commit()
