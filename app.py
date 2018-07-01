from twilio.rest import Client
from flask import Flask, request
from twilio.rest import TwilioRestClient
from twilio.twiml.messaging_response import MessagingResponse
from twilio import twiml

account_sid = 'AC0d2d5b287cb88cb9e20c4d21c599d38a'
auth_token = '9e85d47b90e6ae03275e8447e611f1ee'
client = Client(account_sid, auth_token)

message = client.messages \
          .create(
              body = "This is the Whistle messaging service. Send a picture if you have of any suspected "\
               "ICE related in your neighborhood. Please include the Location and Description in the same message."\
                "Make sure to add a semicolon (;) after the location and the description.",
              from_='+12014705763',
              to='+19178152736' 
              )

print(message.sid);

app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])

def sms_reply():
    resp = MessagingResponse()

    if request.form['NumMedia'] != '0':
        resp.message("Thank you for the tip!")

        return str(resp);
    
if __name__ == "__main__":
    app.run(debug=True);

