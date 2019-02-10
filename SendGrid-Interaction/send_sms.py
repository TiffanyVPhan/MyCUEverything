#!/usr/bin/env python
from twilio.rest import Client
import random
import cgi
form = cgi.FieldStorage()
'''
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
'''

#sendgrid api key: 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

# Your Account SID from twilio.com/console
account_sid = "ACa3802339f5eefb29f7479bfb2aff6a9f"
# Your Auth Token from twilio.com/console
auth_token  = "db9fb2c1d8e3165012492752541e0df7"

client = Client(account_sid, auth_token)

images = ['https://i.ibb.co/ZNznSg8/kitten4.jpg', 'https://i.ibb.co/W6Dmw7X/kitten3.jpg', 'https://i.ibb.co/zQ8GQsc/kitten2.jpg', 'https://i.ibb.co/dQkS15f/kitten1.jpg', 'https://i.ibb.co/MZspDxQ/kitten5.jpg', 'https://i.ibb.co/1ZxnLdS/cat.jpg', 'https://i.ibb.co/bKMTyzH/kitty.jpg', 'https://imgur.com/gallery/lVlPvCB']
num = random.randint(0, 6)

meal_swipes = 3;
if meal_swipes<5:
    message = client.messages.create(
        to="+13035824898",
        from_="+15209001796",
        body="Your meal swipes are running low.")

    print(message.sid)
