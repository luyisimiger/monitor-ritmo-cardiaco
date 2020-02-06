"""configuraciones generales del proyecto"""

class Config(object):
  # REDIS_URL = "redis://redistogo:08121a44b13a2ec1470dd4e86e2d3f19@hammerjaw.redistogo.com:11823"
  REDIS_URL = "redis://localhost"
  RQ_QUEUE_NAME = "monitor-cardiaco"
  PYSERIAL_PORT_WRITE = "/dev/ttyS23"
  PYSERIAL_PORT_READ = "/dev/ttyS24"
