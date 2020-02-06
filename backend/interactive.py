from monitor.managers import SessionManager, MeditionManager
from monitor.task import read_cinturon_data
from monitor.config import Config

sessions = SessionManager()
meditions = MeditionManager()

from redis import Redis
import rq
queue = rq.Queue(Config.RQ_QUEUE_NAME, connection=Redis.from_url(Config.REDIS_URL))
