import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    message_body = request.form['Body'].strip().lower()
    
    # Write the incoming message to a file
    with open("incomingMessage.txt", "w") as file:
        file.write(message_body)
    
    resp = MessagingResponse()
    resp.message("Got it!")
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=False)