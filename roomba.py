import curses
import sys
import struct
import serial
import time

#serialPort = '/dev/ttyUSB0'
serialPort = '/dev/tty.SLAB_USBtoUART'
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
    print ' bot.go('+str(velocity)+','+str(radius)+')'
    self.com.flushInput()
    v = struct.pack(">h",velocity)
    r = struct.pack(">h",radius)
    cmd = ''.join([chr(137),v[0],v[1],r[0],r[1]])
    #cmd = ''.join([chr(137),v[1],v[0],r[1],r[0]])
    self.com.write(cmd+"\r\n")
    return

  def read1line(self):
    return self.com.readline()


def main(*arg):
    screen = curses.initscr()  #we're not in kansas anymore
    curses.noecho()
    curses.curs_set(0)
    screen.timeout(0)
    screen.scrollok(True)
    screenSize = screen.getmaxyx()
    midX = int(screenSize[1]/2)
    screen.keypad(1)  #nothing works without this
    bot = robot()
    print bot.init(serialPort , baudRate)
    # bot.cmnd(''.join(map(chr, [128,132,139,2,0,0])))
    fullmode = [128,132]
    #song = [140,0,4,62,12,66,12,69,12,74,36]
    song = [140,0,1,62,12]
    playsong = [141,0]
    drive = [137,0,00,128,0]
    speed = 200 # maximum 500 mm/s
    bot.cmnd(''.join(map(chr, fullmode+song+playsong)))
    bot.go(0,0)
    press = screen.getch()
    while press != ord('q'):
      press = screen.getch()
      while press == -1:
        press = screen.getch()
      bot.cmnd(''.join(map(chr, song+playsong)))
      if press == ord('j'): #back
        bot.go(-speed,-32768)
        time.sleep(1)
        bot.go(0,0)
      if press == ord('k'): #fwd
        bot.go(speed,-32768)
        time.sleep(1)
        bot.go(0,0)
      if press == ord('h'): #left
        bot.go(speed,1)
        time.sleep(0.5)
        bot.go(0,0)
      if press == ord('l'): #right
        bot.go(speed,-1)
        time.sleep(0.5)
        bot.go(0,0)
      if (press >= ord('0')) & (press <= ord('9')): #set speed
        speed = 50 * (press - 47)

if __name__=='__main__':
    sys.exit(main(*sys.argv))


