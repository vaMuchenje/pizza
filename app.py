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
    engine = create_engine('postgres://hqbydtfyklgvdi:e84dcb01868fc31a6c8ccb2926411bf4532a4b4e141ff96637365c9cbce97544@ec2-54-83-15-95.compute-1.amazonaws.com:5432/de97nb9dek9b26')
    connection = engine.connect()
    cmd = 'INSERT INTO incidents (address, description, incident_lat, incident_lon) VALUES (:address, :description, :lat, :lon)'
    location = request.json['location']
    gmaps = googlemaps.Client(key='AIzaSyAN_7R660HphAES8oxniHvHa4ymuCz32Jc')
    geocode_result = gmaps.geocode(location)
    print(geocode_result[0]['geometry']['location'])
    lat = geocode_result[0]['geometry']['location']['lat']
    lon = geocode_result[0]['geometry']['location']['lng']
    connection.execute(text(cmd), address=location, description=request.json['description'], lat=lat, lon=lon)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
