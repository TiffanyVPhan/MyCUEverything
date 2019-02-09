#!/usr/bin/env python

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
from flask import Flask, request, render_template
app = Flask(__name__)

#sendgrid api key: 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
client = sendgrid.SendGridClient("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")

#flask interaction from form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def add_email():
    email = request.form['emailbox']
    #email = form.getvalue('emailbox')
    meal_swipes = 3;
    if meal_swipes<5:
        message = sendgrid.Mail()
        message.add_to(email)
        message.set_from("myCUEverything@mail")
        message.set_subject("Low number of meal swipes notification")
        message.set_html("Hello, this is an email notifying you that your meal swipes are running low. This means you have less than 5 swipes left. <br><br><br> Opt out of receiving future emails by unsubscribing. <br> Address: Boulder, Colorado 80309")
        client.send(message)


