from flask import Flask, request
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse

app = Flask('joyce_byers')

@app.route('/twilio', methods=['GET', 'POST'])
def hello_world():
    body = request.values.get('Body', None)
    
    response = MessagingResponse()
    response.message("Hello World! You sent: {}".format(body))
    return str(response)