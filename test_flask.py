import flask
from flask import jsonify, request
import pickle
import yaml
from immunity_agent.middlewares.flask_middleware import ImmunityFlaskMiddleware

app = flask.Flask(__name__)
app.wsgi_app = ImmunityFlaskMiddleware(app.wsgi_app, app)

users = [
    {"id": 1, "name": "Иван Иванов", "email": "ivan@example.com"},
    {"id": 2, "name": "Петр Петров", "email": "petr@example.com"},
]

next_id = len(users) + 1


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


@app.route("/users", methods=["POST"])
def create_user():
    global next_id
    data = request.json
    new_user = {"id": next_id, "name": data["name"], "email": data["email"]}
    users.append(new_user)
    next_id += 1
    return jsonify(new_user), 201


@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    found_user = None
    for user in users:
        if user["id"] == id:
            found_user = user
            break

    if not found_user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    found_user.update(data)
    return jsonify(found_user)


@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    found_index = None
    for i, user in enumerate(users):
        if user["id"] == id:
            found_index = i
            break

    if found_index is None:
        return jsonify({"error": "User not found"}), 404

    del users[found_index]
    return "", 204

@app.route('/deserialize/1/', methods=['POST'])
def vulnerable_route_1():
    data = request.form['data'].encode()

    # Проверяем длину данных
    if len(data) == 0:
        return "No data provided."

    # Десериализуем данные с помощью pickle
    try:
        deserialized_data = pickle.loads(data)
    except EOFError:
        return "Invalid or incomplete data."

    return f'Deserialized data: {deserialized_data}'

@app.route('/deserialize/2/', methods=['POST'])
def vulnerable_route_2():
    data = request.form['data']
    # Десериализуем данные с помощью yaml
    deserialized_data = yaml.load(data, Loader=yaml.FullLoader)
    return f'Deserialized data: {deserialized_data}'

class VulnerableObject:
    def __reduce__(self):
        return (eval, ("__import__('os').system('ls')",))

@app.route('/deserialize/3/', methods=['POST'])
def vulnerable_route_3():
    data = request.form['data']
    try:
        deserialized_data = pickle.loads(data.encode())
        return f'Deserialized object: {deserialized_data}'
    except Exception as e:
        return f'Error: {e}'

if __name__ == "__main__":
    app.run(debug=True)
