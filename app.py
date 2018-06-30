from flask import Flask, request, jsonify
app = Flask(__name__)
import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text

@app.route('/')
def homepage():
    return "hii"

@app.route('/witness/', methods=["POST"])
def witness():
    engine = create_engine('postgres://hqbydtfyklgvdi:e84dcb01868fc31a6c8ccb2926411bf4532a4b4e141ff96637365c9cbce97544@ec2-54-83-15-95.compute-1.amazonaws.com:5432/de97nb9dek9b26')
    connection = engine.connect()
    
    # This is just sample code to show that db connection works
    cmd = 'select * from subscribers where id > :id'
    id = 0
    subscribers = connection.execute(text(cmd), id=id)
    for subscriber in subscribers: print(subscriber)
    #TODO: Parse location
    #TODO: insert into database
    print('Location: ', location)
    print('Description: ', description)
    return jsonify(success=True)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
