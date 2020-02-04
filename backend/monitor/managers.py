import math
import time
import sys
from tinydb import TinyDB, where
from tinydb.middlewares import Middleware

DATABASE_FILE = "monitor.json"


class DocumentWithIdMiddleware(Middleware):
  
  def read(self):
    data = self.storage.read()

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
      "datestart": self.estampa()
    })

    return self.get(id)

  def close(self, id):
    
    self.table.update({
      "dateclose": self.estampa()
    }, doc_ids=[id])

    return self.get(id)

  def get(self, id):
    doc = self.table.get(doc_id=id)
    return doc

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
    return self.table.search( ~(where("dateclose").exists()) )


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
  
  def all(self, sessionid):
    return self.table.search(where("sessionid") == sessionid)

  @staticmethod
  def detail(meditions):
    total = 0
    
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
      
      # promedio: sumatoria de los datos
      sumrh += m.rh
      maxrh = maxrh if maxrh >= m.rh else m.rh
      minrh = minrh if minrh <= m.rh else m.rh

      sumrr += m.rr
      maxrr = maxrr if maxrr >= m.rr else m.rr
      minrr = minrr if minrr <= m.rr else m.rr

    
    # promedio: division sobre el total de datos
    avgrh = 0 if total == 0 else sumrh / total
    avgrr = 0 if total == 0 else sumrr / total

    # desviacion estandar: sum de diferencia de cuadrados
    for m in meditions:
      ssumrh += (m.rh - avgrh) ** 2
      ssumrr += (m.rr - avgrr) ** 2

    # desviacion estandar: division sobre el total de datos
    srh = 0 if total >= 0 else ssumrh / total
    srr = 0 if total >= 0 else ssumrr / total

    # desviacion estandar: raiz cuadrada
    srh = math.sqrt(srh)
    srr = math.sqrt(srr)

    return {
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