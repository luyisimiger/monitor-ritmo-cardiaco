from flask import Flask
from flask_cors import cross_origin
from . import device

app = Flask(__name__)

@app.route('/')
def index():
    return "flask app running"


@app.route('/device/readdata')
@cross_origin()
def readdata():
    return device.read_data()
