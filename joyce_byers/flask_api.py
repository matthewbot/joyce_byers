from flask import Flask, request
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse

app = Flask('joyce_byers')
app.message_callback = None

@app.route('/twilio', methods=['GET', 'POST'])
def twilio():
    body = request.values.get('Body', None)

    assert app.message_callback is not None
    ok = app.message_callback(body)

    if not ok:
        response = MessagingResponse()
        response.message('The monster is busy right now! Try again later.')
        return str(response)
    else:
        return ('', 204)