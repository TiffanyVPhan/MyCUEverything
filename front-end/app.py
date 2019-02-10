from uuid import uuid4
from flask import Flask, render_template, request, redirect, make_response

from api.mycueverything import MyCUEverything

app = Flask(__name__)
app.secret_key = 'dev'

everythings = {}


@app.route('/')
def index():
    if everythings.get(request.cookies['session'], None):
        return redirect('/dash')

    response = make_response(render_template('index.html'))
    response.set_cookie('session', str(uuid4()))
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    everythings[request.cookies['session']] = MyCUEverything(request.form['username'],
                                                             request.form['password'])
    return redirect('dash')


@app.route('/logout')
def logout():
    everythings.pop(request.cookies['session'])
    return redirect('/')


@app.route('/dash')
def dash():
    return render_template('dash.html', everything=everythings[request.cookies['session']])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
