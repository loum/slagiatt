"""SLAGIATT main application file.
"""
import os
import flask
import flask_restless

import slagiatt.route
import slagiatt.common
import slagiatt.model


APP = flask.Flask(__name__)

if os.environ.get('SLAGIATT_CONF'):
    APP.config.from_envvar('SLAGIATT_CONF')
else:
    APP.config.from_object('slagiatt.config')

slagiatt.common.DB.init(target=APP.config.get('SQLALCHEMY_DATABASE_URI'))
slagiatt.common.BASE.metadata.bind = slagiatt.common.DB.engine
slagiatt.common.BASE.metadata.create_all()

# Register the DB-based APIs.
MANAGER = flask_restless.APIManager(APP, session=slagiatt.common.SESSION)
MANAGER.create_api(slagiatt.model.Device,
                   methods=['GET', 'POST', 'DELETE'])

# Register the traditional APIs.
APP.register_blueprint(slagiatt.route.health)


@APP.cli.command('initdb')
def initdb_command():
    """CLI wrapper to initialise the database.

    """
    slagiatt.common.BASE.metadata.create_all()
