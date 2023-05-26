from flask import Flask, jsonify, make_response
from services.auth import auth_routes
from services.question import question_routes

app = Flask(__name__)

app.register_blueprint(auth_routes, url_prefix='/client')
app.register_blueprint(question_routes, url_prefix='/client')

@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
