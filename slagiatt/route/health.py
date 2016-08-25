import flask


health = flask.Blueprint('health', __name__)

@health.route('/health', methods=['GET'])
def status():
    return flask.jsonify("Hey, I'm OK")
