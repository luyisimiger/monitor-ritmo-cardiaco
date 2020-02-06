from monitor.arduino import ArduinoCard
from monitor.config import Config

if __name__ == "__main__":
  card = ArduinoCard(Config.PYSERIAL_PORT_WRITE)
  card.turnon()
