import numpy as np
import statistics
import sys
from sklearn.cluster import KMeans


def detail_session(manager, id):
  doc = manager.get(id)
  meditions = manager.meditions.all(id)
  detail = detail_meditions(meditions)

  doc["detail"] = detail
  doc["meditions"] = meditions
  
  return doc


def detail_meditions(meditions):
  total = 0
  mindate = None
  maxdate = None
  
  sumrh = 0
  maxrh = 0
  minrh = sys.maxsize
  avgrh = 0
  srh = 0

  sumrr = 0
  maxrr = 0
  minrr = sys.maxsize
  avgrr = 0
  srr = 0

  auxrh = []
  auxrr = []
  
  for m in meditions:
    total += 1

    auxrh.append( m["rh"])
    auxrr.append(m["rr"])

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
  avgrh = round( 0 if total == 0 else sumrh / total , 2)
  avgrr = round( 0 if total == 0 else sumrr / total , 2)

  if len(auxrh) >= 2:
    srh = round( statistics.stdev(auxrh) , 2)
    srr = round( statistics.stdev(auxrr) , 2)

    dataRH = np.array( [ [i, rh] for i, rh in enumerate(auxrh, start=1)] )
    kmeansRH = KMeans(n_clusters=2)
    kmeansRH.fit(dataRH)
    centroidesRH = kmeansRH.cluster_centers_
    rh_centroid1 = round(centroidesRH[0][1], 2)
    rh_centroid2 = round(centroidesRH[1][1], 2)

    dataRR = np.array( [ [i, rr] for i, rr in enumerate(auxrr, start=1)])
    kmeansRR = KMeans(n_clusters=2)
    kmeansRR.fit(dataRR)
    centroidesRR = kmeansRR.cluster_centers_
    rr_centroid1 = round(centroidesRR[0][1], 2)
    rr_centroid2 = round(centroidesRR[1][1], 2)

  else:
    srh = 0
    srr = 0
    rh_centroid1 = 0
    rh_centroid2 = 0
    rr_centroid1 = 0
    rr_centroid2 = 0


  return {
    "datestart": mindate,
    "dateend": maxdate,
    "rh": {
      "average": avgrh,
      "max": maxrh,
      "min": minrh,
      "sigma": srh,
      "centroid1": rh_centroid1,
      "centroid2": rh_centroid2
    },
    "rr": {
      "average": avgrr,
      "max": maxrr,
      "min": minrr,
      "sigma": srr,
      "centroid1": rr_centroid1,
      "centroid2": rr_centroid2
    }
  }
