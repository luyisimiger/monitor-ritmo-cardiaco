from time import sleep
import serial
from .device import read_data


class ArduinoCard:

  def __init__(self, portcom):
    self.serial = serial.Serial(portcom, 9600)
    self.capture = False

  def turnon(self):
    self.capture = True
    self.run()

  def turnoff(self):
    self.capture = False
  
  def run(self):
    
    while self.capture:
      self.loop()
      sleep(3)

    self.serial.close()
  
  def loop(self):
    data = read_data()
    message = str(data) + "\n"
    self.serial.write(message.encode("raw_unicode_escape"))
    print("data", data)
    # self.serial.write(str(message).encode("utf-8"))
