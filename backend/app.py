from flask import Flask
from . import device

app = Flask(__name__)

@app.route('/')
def index():
    return "flask app running"


@app.route('/device/readdata')
def readdata():
    return device.read_data()
