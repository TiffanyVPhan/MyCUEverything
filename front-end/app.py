from flask import Flask, render_template, request, redirect, session

from api.mycueverything import MyCUEverything

app = Flask(__name__)
app.secret_key = 'dev'

everythings = {}


@app.route('/')
def index():
    # Store a dummy value so that a session key is created.
    session['id'] = 1

    if everythings[request.cookies['session']]:
        return redirect('/dash')
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
    return render_template('dash.html', everything=everythings[request.cookies['session']],
                                        test=everythings[request.cookies['session']].student_id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
