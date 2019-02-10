from uuid import uuid4
from flask import Flask, render_template, request, redirect, make_response

from api.mycueverything import MyCUEverything

app = Flask(__name__)
app.secret_key = 'dev'

everythings = {}


@app.route('/')
def index():
    if everythings.get(request.cookies.get('session', None), None):
        return redirect('/dash')

    response = make_response(render_template('index.html'))
    response.set_cookie('session', str(uuid4()))
    return response


@app.route('/login', methods=['POST'])
def login():
    if not request.form.get('username', None) or not request.form.get('password', None):
        return redirect('/?error')
    if '@colorado.edu' in request.form.get('username', ''):
        request.form['username'] = request.form['username'].replace('@colorado.edu', '')

    everythings[request.cookies['session']] = MyCUEverything(request.form['username'],
                                                             request.form['password'])
    return redirect('dash')


@app.route('/logout')
def logout():
    if request.cookies.get('session', None):
        everythings.pop(request.cookies['session'])

    return redirect('/')


@app.route('/dash')
def dash():
    if not everythings.get(request.cookies.get('session', None), None):
        return redirect('/')

    return render_template('dash.html', everything=everythings[request.cookies['session']])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
