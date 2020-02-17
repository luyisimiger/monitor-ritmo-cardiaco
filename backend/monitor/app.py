from flask import Flask
from flask_cors import cross_origin, CORS
from redis import Redis
import rq

from . import device
from .managers import SessionManager
from .config import Config
from .logic import detail_session


app = Flask(__name__)
app.config.from_object(Config)
app.redis = Redis.from_url(app.config['REDIS_URL'])
app.task_queue = rq.Queue(app.config['RQ_QUEUE_NAME'], connection=app.redis)

cors = CORS(app)

def fn_launch_job_session(session):
  meta = { "session_opened": True }
  app.task_queue.enqueue("backend.monitor.task.read_cinturon_data", session, job_id=session["id"], job_timeout="24h", meta=meta)


@app.route('/')
def index():
    return "flask app running"


@app.route('/device/readdata')
@cross_origin()
def readdata():
    return device.read_data()


@app.route('/sessions/open')
def session_open():
  sessions_manager = SessionManager()
  session = sessions_manager.open()
  fn_launch_job_session(session)

  return session


@app.route('/sessions/<int:id>/capture')
def session_capture(id):
  sessions_manager = SessionManager()
  session = sessions_manager.set_status(id, "open")
  fn_launch_job_session(session)

  return session


@app.route('/sessions/<int:id>')
@app.route('/sessions/<int:id>/detail')
def session_detail(id):
  sessions_manager = SessionManager()
  session = detail_session(sessions_manager, id)

  return session


@app.route('/sessions/<int:id>/close')
def session_close(id):
  sessions_manager = SessionManager()
  session = sessions_manager.close(id)
  job = app.task_queue.fetch_job(session["id"])
  job.meta["session_opened"] = False
  job.save_meta()

  return session


@app.route('/sessions/<int:id>/remove')
def session_remove(id):
  sessions_manager = SessionManager()
  session = detail_session(sessions_manager, id)
  sessions_manager.remove(id)
  return session


@app.route('/sessions')
def session_all():
  sessions_manager = SessionManager()
  response = {}
  response["result"] = sessions_manager.all()

  return response


@app.route('/sessions/opened')
def session_opened():
  sessions_manager = SessionManager()
  response = {}
  response["result"] = sessions_manager.all_opened()

  return response


@app.route('/sessions/full')
def session_all_full():
  sessions_manager = SessionManager()
  sessions = sessions_manager.all()

  response = {}
  response["result"] = [ detail_session(sessions_manager, int(s["id"])) for s in sessions]

  return response