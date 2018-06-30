import settings
from flask import Flask, request, jsonify
app = Flask(__name__)
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    return "hii"

@app.route('/witness/', methods=["POST"])
def web_witness():
    location = request.json['location']
    description = request.json['description']

    #TODO: Parse location

    #TODO: insert into database
    print('Location: ', location)
    print('Description: ', description)
    return jsonify(success=True)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
