import math
import time
import sys
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

  def close(self, id):
    
    self.table.update({
      "status": "close"
    }, doc_ids=[id])

    return self.get(id)

  def get(self, id):
    doc = self.table.get(doc_id=id)
    return doc

  def remove(self, id):
    self.meditions.remove(id)
    self.table.remove(doc_ids=[id])

  def detail(self, id):
    doc = self.get(id)
    meditions = self.meditions.all(id)
    detail = self.meditions.detail(meditions)

    doc["detail"] = detail
    doc["meditions"] = meditions

    return doc

  def all(self):
    return self.table.all()

  def all_opened(self):
    return self.table.search( where("status") == "open" )

  def all_full(self):
    sessions = self.all()
    return [self.detail(int(s["id"])) for s in sessions]


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

  @staticmethod
  def detail(meditions):
    total = 0
    mindate = None
    maxdate = None
    
    sumrh = 0
    maxrh = 0
    minrh = sys.maxsize
    avgrh = 0
    ssumrh = 0
    srh = 0

    sumrr = 0
    maxrr = 0
    minrr = sys.maxsize
    avgrr = 0
    ssumrr = 0
    srr = 0
    
    for m in meditions:
      total += 1

      # initialization
      mindate = m["date"] if mindate is None else mindate
      maxdate = m["date"] if maxdate is None else maxdate
      
      # promedio: sumatoria de los datos
      sumrh += m["rh"]
      maxrh = maxrh if maxrh >= m["rh"] else m["rh"]
      minrh = minrh if minrh <= m["rh"] else m["rh"]

      sumrr += m["rr"]
      maxrr = maxrr if maxrr >= m["rr"] else m["rr"]
      minrr = minrr if minrr <= m["rr"] else m["rr"]

      # fechas: maximo y minimo
      maxdate = maxdate if maxdate >= m["date"] else m["date"]
      mindate = mindate if mindate <= m["date"] else m["date"]
    
    # promedio: division sobre el total de datos
    avgrh = 0 if total == 0 else sumrh / total
    avgrr = 0 if total == 0 else sumrr / total

    # desviacion estandar: sum de diferencia de cuadrados
    for m in meditions:
      ssumrh += (m["rh"] - avgrh) ** 2
      ssumrr += (m["rr"] - avgrr) ** 2

    # desviacion estandar: division sobre el total de datos
    srh = 0 if total >= 0 else ssumrh / total
    srr = 0 if total >= 0 else ssumrr / total

    # desviacion estandar: raiz cuadrada
    srh = math.sqrt(srh)
    srr = math.sqrt(srr)

    return {
      "datestart": maxdate,
      "dateend": mindate,
      "rh": {
        "average": avgrh,
        "max": maxrh,
        "min": minrh,
        "sigma": srh
      },
      "rr": {
        "average": avgrr,
        "max": maxrr,
        "min": minrr,
        "sigma": srr
      }
    }