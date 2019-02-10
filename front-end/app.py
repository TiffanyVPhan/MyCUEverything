from flask import Flask, render_template, request, session, redirect

from api.mycueverything import MyCUEverything

app = Flask(__name__)
app.secret_key = 'dev'

everythings = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    everythings[request.cookies['session']] = MyCUEverything(request.form['username'],
                                                             request.form['password'])
    return redirect('dash')


@app.route('/dash')
def dash():
    return render_template('dash.html', everything=everythings[request.cookies['session']])


if __name__ == '__main__':
    app.run(debug=True)
