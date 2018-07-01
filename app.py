from flask import Flask, request, jsonify
app = Flask(__name__)
import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text
import googlemaps
from datetime import datetime
from twilio.rest import TwilioRestClient
from twilio.twiml.messaging_response import MessagingResponse
from twilio import twiml
from twilio.rest import Client
account_sid = 'AC0d2d5b287cb88cb9e20c4d21c599d38a'
auth_token = '9e85d47b90e6ae03275e8447e611f1ee'
client = Client(account_sid, auth_token)
from flask import render_template

engine = create_engine('postgres://hqbydtfyklgvdi:e84dcb01868fc31a6c8ccb2926411bf4532a4b4e141ff96637365c9cbce97544@ec2-54-83-15-95.compute-1.amazonaws.com:5432/de97nb9dek9b26')
connection = engine.connect()

message = client.messages \
          .create(
              body = "This is the Whistle messaging service. Send a picture if you have of any suspected "\
               "ICE related in your neighborhood. Please include the Location and Description in the same message."\
                "Make sure to add a semicolon (;) after the location and the description.",
              from_='+12014705763',
              to='+19178152736'
              )

print(message.sid);

@app.route('/')
def homepage():
    return "hii"

# This is needed to Allow CORS
@app.route('/witness/', methods=['GET'])
def witness_get():
    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/witness/', methods=["POST"])
def witness():
    cmd = 'INSERT INTO incidents (address, description, incident_lat, incident_lon) VALUES (:address, :description, :lat, :lon)'
    location = request.json['location']
    gmaps = googlemaps.Client(key='AIzaSyAN_7R660HphAES8oxniHvHa4ymuCz32Jc')
    geocode_result = gmaps.geocode(location)
    print(geocode_result[0]['geometry']['location'])
    lat = geocode_result[0]['geometry']['location']['lat']
    lon = geocode_result[0]['geometry']['location']['lng']
    connection.execute(text(cmd), address=location, description=request.json['description'], lat=lat, lon=lon)

    cmd_get_subscribers = 'SELECT area_lat, area_lon, phone_number FROM subscribers'
    result = connection.execute(cmd_get_subscribers)
    for subscriber in result:
        try:
            client.messages \
                .create(
                body=request.json['description'] + " at " + request.json['location'],
                from_='+12014705763',
                to=subscriber[2]
            )
        except Exception as e:
            print(e.__doc__)
            print(e)
    return jsonify(success=True)

@app.route('/sms', methods=['GET', 'POST'])
def sms_reply():
    print(request.form['Body'])
    resp = MessagingResponse()
    resp.message("Thank you for the tip!")
    return str(resp)

@app.route('/map', methods=['GET'])
def map():
    incident_id = request.args.get('incident_id', None)
    cmd = "select * from incidents"
    incidents_result = connection.execute(text(cmd))
    incident_addresses = []
    incident_descriptions = []

    incident_lats = []
    incident_lons = []
    for incident in incidents_result:
        incident_addresses.append(incident[1])
        incident_descriptions.append(incident[2])
        incident_lats.append(incident[4])
        incident_lons.append(incident[5])
    if incident_id is not None:
        return render_template('map.html', incident_id=incident_id, incident_addresses=incident_addresses, incident_descriptions=incident_descriptions, incident_lats=incident_lats, incident_lons=incident_lons)
    else:
        return render_template('map.html', incident_addresses=incident_addresses, incident_descriptions=incident_descriptions, incident_lats=incident_lats, incident_lons=incident_lons)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
