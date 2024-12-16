import flask
from immunity_agent.middlewares.flask_middleware import ImmunityFlaskMiddleware

app = flask.Flask(__name__)
app.wsgi_app = ImmunityFlaskMiddleware(app.wsgi_app)

@app.route('/', methods=['GET'])
def home():
        return "<h1>Hello World!</h1>"

@app.route('/test1', methods=['GET'])
def test1():
    print("Handler: Test 1")
    return "Test 1"

# Обработчик для теста
@app.route('/test2', methods=['GET'])
def test2():
    print("Handler: Test 2")
    return "Test 2"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
