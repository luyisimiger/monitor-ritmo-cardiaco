import math
import time
from tinydb import TinyDB, where
from tinydb.middlewares import Middleware


DATABASE_FILE = "monitor.json"


class DocumentWithIdMiddleware(Middleware):
  
  def read(self):
    data = self.storage.read()

    if data is None:
      return data

    for table_name in data:
      table = data[table_name]

      for doc_id in table:
        item = table[doc_id]
        item["id"] = doc_id # the reason for the middleware

    return data

  def write(self, data):
    self.storage.write(data)

  def close(self):
    self.storage.close()


class BaseManager:

  def __init__(self, tablename, db=None):
    
    self.db = db or TinyDB(DATABASE_FILE, storage=DocumentWithIdMiddleware(TinyDB.DEFAULT_STORAGE))
    self.table = self.db.table(tablename)

  def estampa(self):
    return time.time() * 1000


class SessionManager(BaseManager):

  def __init__(self):
    super().__init__("sessions")
    self.meditions = MeditionManager(self.db)

  def open(self):

    id = self.table.insert({
      "status": "open"
    })

    return self.get(id)

  def set_status(self, id, status):
    self.table.update({
      "status": status
    }, doc_ids=[id])

    return self.get(id)

  def close(self, id):
    return self.set_status(id, "close")

  def get(self, id):
    doc = self.table.get(doc_id=id)
    return doc

  def remove(self, id):
    self.meditions.remove(id)
    self.table.remove(doc_ids=[id])

  def all(self):
    return self.table.all()

  def all_opened(self):
    return self.table.search( where("status") == "open" )


class MeditionManager(BaseManager):

  def __init__(self, db=None):
    super().__init__("meditions", db=db)

  def save(self, sessionid, rh, rr):
    return self.table.insert({
      "sessionid": sessionid,
      "date": self.estampa(),
      "rh": rh,
      "rr": rr
    })
  
  def remove(self, sessionid):
    self.table.remove(where("sessionid") == str(sessionid))

  def all(self, sessionid):
    return self.table.search(where("sessionid") == str(sessionid))
