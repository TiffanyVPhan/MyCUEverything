from flask import Flask, render_template, request, session
from flask.ext.session import Session

app = Flask(__name__)
Session(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
