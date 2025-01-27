import flask
from flask import jsonify, request
import pickle
from yaml import *
from immunity_agent.middlewares.flask_middleware import ImmunityFlaskMiddleware
import base64
import sys
sys.setrecursionlimit(150000)
app = flask.Flask(__name__)
app.wsgi_app = ImmunityFlaskMiddleware(app.wsgi_app, app)

@app.route('/deserialize/1/', methods=['POST'])
def vulnerable_route_1():

    data = request.form['data']

    # Декодирование данных Base64
    decoded_data = base64.b64decode(data.encode('utf-8'))

    # Десериализация данных с помощью pickle
    try:
        deserialized_data = pickle.loads(decoded_data)
        return f"Десериализированные данные: {deserialized_data}"
    except Exception as e:
        return f"Ошибка десериализации: {e}", 500

@app.route('/deserialize/2/', methods=['POST'])
def vulnerable_route_2():

    data = request.form['data']
    # Десериализуем данные с помощью yaml
    deserialized_data = unsafe_load(data)
    return f'Deserialized data: {deserialized_data}'

def recursive_function(n):
    if n == 0:
        return 1
    else:
        return n * recursive_function(n - 1)

@app.route('/resource/1/', methods=['GET'])
def resource():

    n = int(request.args.get('n', default=10))
    result = recursive_function(n)
    return f'Factorial of {n}: {result}'

@app.route('/debug')
def debug_mode():

    app.config['DEBUG'] = True
    return 'Debug mode enabled'

@app.route('/show_debug')
def show_debug_mode():

    return str(app.config['DEBUG'])

if __name__ == "__main__":
    app.run(debug=False)
