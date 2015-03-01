import sys
import struct
import serial
import time

serialPort = '/dev/ttyUSB0'
baudRate = 57600

class robot:

  def init(self, serialPort , baudRate):
    try:
      self.com = serial.Serial(serialPort, baudRate, timeout = 1)
    except:
      return "fail to open "+serialPort
    return "opened "+serialPort+" at "+str(baudRate)+" baud"

  def cmnd(self, cmd):
    self.com.flushInput()
    self.com.write(cmd+"\r\n") # not cmd[:-1]+"\r\n")
    return #self.com.readlines()

  def go(self, velocity, radius):
    self.com.flushInput()
    v = struct.pack(">h",velocity)
    r = struct.pack(">h",radius)
    cmd = ''.join([chr(137),v[0],v[1],r[0],r[1]])
    self.com.write(cmd+"\r\n")
    return

  def read1line(self):
    return self.com.readline()

def main(*arg):
    bot = robot()
    print bot.init(serialPort , baudRate)
    # bot.cmnd(''.join(map(chr, [128,132,139,2,0,0])))
    fullmode = [128,132]
    song = [140,0,4,62,12,66,12,69,12,74,36]
    playsong = [141,0]
    drive = [137,0,00,128,0]
    bot.cmnd(''.join(map(chr, fullmode+song+playsong)))
    bot.go(200,0)
    time.sleep(2)
    bot.go(0,0)


if __name__=='__main__':
    sys.exit(main(*sys.argv))


