import random

def read_data():
  rh = random.randint(100, 170)
  rr = random.randint(500, 700)

  return {
    "rh": rh,
    "rr": rr
  }
