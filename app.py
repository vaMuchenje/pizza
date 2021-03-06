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
from haversine import haversine
account_sid = 'twilio_sid_goes_here'
auth_token = 'twilio_token_goes_here'
client = Client(account_sid, auth_token)
from flask import render_template

engine = create_engine('postgres_url_goes_here')
connection = engine.connect()

invalid_input_error = "Welcome to Whistle. Respond if you see an unsafe incident. Please use this format: ICE raid description; 285 DeKalb Ave subway"
invalid_address_error = "Welcome to Whistle. Please give more specific address. Please use this format: ICE raid description; 285 DeKalb Ave subway"
message = client.messages \
          .create(
              body = invalid_input_error,
              from_='+12014705763',
              to='+19178152736'
              )

print(message.sid);
gmaps = googlemaps.Client(key='google_maps_key_goes_here')

@app.route('/')
def homepage():
    return "hii"

# This is needed to Allow CORS
@app.route('/witness/', methods=['GET'])
def witness_get():
    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def add_incident(address, description):
    geocode_result = gmaps.geocode(address)
    print(geocode_result)
    if len(geocode_result) == 0:
        return False
    lat = geocode_result[0]['geometry']['location']['lat']
    lon = geocode_result[0]['geometry']['location']['lng']
    cmd = 'INSERT INTO incidents (address, description, incident_lat, incident_lon) VALUES (:address, :description, :lat, :lon)'
    connection.execute(text(cmd), address=address, description=description, lat=lat, lon=lon)
    cmd_get_subscribers = 'SELECT area_lat, area_lon, phone_number, radius FROM subscribers'
    result = connection.execute(cmd_get_subscribers)
    for subscriber in result:
        try:
            distance_from_user_to_event = haversine((lat, lon), (subscriber[0], subscriber[1]), miles=True)
            print("Distance to user " + subscriber[2] + " is " + str(distance_from_user_to_event))
            if distance_from_user_to_event < subscriber[3]:
              client.messages \
                  .create(
                  body="Whistle alert: "+description + " at " + address + ". Click to find out more: https://bit.ly/2KE98GC",
                  from_='+12014705763',
                  to=subscriber[2]
              )
        except Exception as e:
            print(e.__doc__)
            print(e)
            return False
    return True

@app.route('/witness/', methods=["POST"])
def witness():
    location = request.json['location']
    description = request.json['description']
    add_incident(location, description)
    return jsonify(success=True)

@app.route('/sms', methods=['GET', 'POST'])
def sms_reply():
    print(request.form['Body'])
    body = request.form['Body']
    resp = MessagingResponse()
    splitted_body = body.split(';')
    if (";" not in body) or (len(splitted_body) != 2):
        resp.message(invalid_input_error)
    else:
        description = splitted_body[0]
        address = splitted_body[1]
        print("desc" + description)
        print("address" + address)
        try:
            print('going to add incident')
            success = add_incident(address, description)
            if success:
                resp.message('Thank you, we will alert the community')
            else:
                resp.message(invalid_address_error)
        except Exception as e:
            resp.message(invalid_input_error)
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
