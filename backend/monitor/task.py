import serial
import json
from rq import get_current_job

from .arduino import ArduinoCard
from .config import Config
from .managers import MeditionManager

def read_cinturon_data(session):
  
  job = get_current_job()
  ser = serial.Serial(Config.PYSERIAL_PORT_READ, 9600)
  medition = MeditionManager()
  count = 0

  while job.meta["session_opened"]:
    raw_data = ser.readline()
    json_acceptable_string = raw_data.decode("raw_unicode_escape").replace("'", "\"")
    data = json.loads(json_acceptable_string)
    medition.save(job.id, data["rh"], data["rr"])

    print("read", data)
    count += 1
    job.refresh()

  ser.close()
  medition.db.close()
  return count
