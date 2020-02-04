from flask import Flask
from flask_cors import cross_origin
from . import device
from .managers import SessionManager


app = Flask(__name__)


@app.before_first_request
def start_arduino_receiver():
  print("start_arduino_receiver")


@app.route('/')
def index():
    return "flask app running"


@app.route('/device/readdata')
@cross_origin()
def readdata():
    return device.read_data()


@app.route('/sesssions/open')
def session_open():
  sessions = SessionManager()
  session = sessions.open()

  return session


@app.route('/sesssions/<int:id>')
def session_single(id):
  sessions = SessionManager()
  session = sessions.get(id)

  return session


@app.route('/sesssions/<int:id>/detail')
def session_detail(id):
  sessions = SessionManager()
  session = sessions.detail(id)

  return session


@app.route('/sesssions/<int:id>/close')
def session_close(id):
  sessions = SessionManager()
  session = sessions.close(id)

  return session


@app.route('/sesssions')
def session_all():
  sessions = SessionManager()
  response = {}
  response["result"] = sessions.all()

  return response


@app.route('/sesssions/opened')
def session_opened():
  sessions = SessionManager()
  response = {}
  response["result"] = sessions.all_opened()

  return response
