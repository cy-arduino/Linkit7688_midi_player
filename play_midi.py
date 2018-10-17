import sys
import os 
import serial
import time
import binascii
from subprocess import call
from time import sleep

pitch_freq = {'60':'523','62':'587','64':'659','65':'698','67':'784','69':'880','71':'988'}

tmpfile = 'tmp.txt'

if len(sys.argv) < 2:
  print 'Usage: ' + sys.argv[0] + ' <.mid file>'
  sys.exit(1)

midiFile = sys.argv[1]


os.system('rm -rf ' + 'tmp.txt')
os.system('mididump.py ' + midiFile + ' > tmp.txt')


with open('tmp.txt', 'r') as f:
 with serial.Serial('/dev/ttyS0', 57600) as s:

  for line in f:

    if 'midi.NoteOnEvent' not in line:
      continue
    #print line

    idx = line.find('tick=')
    if -1 != idx:
      tick = line[idx + 5:].split(', ')[0]
      #print 'tick: ' + tick

    idx = line.find('channel=')
    if -1 != idx:
      channel = line[idx + 8:].split(', ')[0]
      #print 'channel: ' + channel
      if '0' != channel:
        print 'ignore channel ' + channel
        continue

    idx = line.find('data=[')
    if -1 != idx:
      pitch = line[idx + 6:].split(', ')[0]
      #print 'pitch: ' + pitch

      volume = line[idx + 6:].split(', ')[1].split(']')[0]
      #print 'volume: ' + volume

    sleep(float(tick)/1000)
    print 'pitch: ' + pitch
    print 'freq: ' + pitch_freq[pitch]
    print 'volume: ' + volume
    

    s.write('n\n')
    s.write('f ' + pitch_freq[pitch] + '\n')

    if int(volume) >= 0:
      s.write('t\n')

  s.write('n\n')
  s.write('n\n')
  s.write('n\n')
