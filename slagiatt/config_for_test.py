"""Testing configuration file.

"""
import tempfile


DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(tempfile.mkstemp()[1])
