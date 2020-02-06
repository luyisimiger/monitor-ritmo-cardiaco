from flask import Flask
from flask_cors import cross_origin
from redis import Redis
import rq

from . import device
from .managers import SessionManager
from .config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.redis = Redis.from_url(app.config['REDIS_URL'])
app.task_queue = rq.Queue(app.config['RQ_QUEUE_NAME'], connection=app.redis)


def fn_launch_job_session(session):
  meta = { "session_opened": True }
  job = app.task_queue.enqueue("backend.monitor.task.read_cinturon_data", session, job_id=session["id"], job_timeout="24h", meta=meta)


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
  fn_launch_job_session(session)

  return session


@app.route('/sesssions/<int:id>/capture')
def session_capture(id):
  sessions = SessionManager()
  session = sessions.get(id)
  fn_launch_job_session(session)

  return session


@app.route('/sesssions/<int:id>')
@app.route('/sesssions/<int:id>/detail')
def session_detail(id):
  sessions = SessionManager()
  session = sessions.detail(id)

  return session


@app.route('/sesssions/<int:id>/close')
def session_close(id):
  sessions = SessionManager()
  session = sessions.close(id)
  job = app.task_queue.fetch_job(session["id"])
  job.meta["session_opened"] = False
  job.save_meta()

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
