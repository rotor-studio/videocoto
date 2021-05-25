from pathlib import Path
from time import sleep
import time
from array import *
import os
import csv
from omxplayer.player import OMXPlayer
import logging
logging.basicConfig(level=logging.INFO)
from pythonosc import udp_client
import argparse
import math
import threading
from pythonosc import dispatcher
from pythonosc import osc_server
from typing import List, Any

#global
step = 0
now = 0
play = False
destPort = 0
portIn = 8000
destIp = array('i')
stepVideo = array('l')
videoNow = " "
vidNow = 0
playing = 0



#Get Values from OSC
def getOsc(adress, *args):
     vidNow = int(args[0])
     print ("Recibe para play ahora >> "+str(vidNow))
     playVideos(vidNow)
     
#Prevencion de errores si no hay puertos de destino
def handle_error(self, request, client_address):
    """Handle an exception in the Server's callbacks gracefully.
    Writes the error to sys.stderr and, if the error_prefix (see setSrvErrorPrefix()) is set,
    sends the error-message as reply to the client
    """
    (e_type, e) = sys.exc_info()[:2]
    self.printErr("%s on request from %s: %s" % (e_type.__name__, getUrlStr(client_address), str(e)))

    if self.print_tracebacks:
        import traceback
        traceback.print_exc() # XXX But this goes to stderr!

    if len(self.error_prefix):
        self.sendOSCerror("%s: %s" % (e_type.__name__, str(e)), client_address)

     
def print_fader_handler(unused_addr, args, value):
    print("[{0}] ~ {1:0.2f}".format(args[0], value))


def print_xy_fader_handler(unused_addr, args, value1, value2):
    print("[{0}] ~ {1:0.2f} ~ {2:0.2f}".format(args[0], value2, value1))

#Listen OSC
if __name__ == "__main__":
    
 
     dispatcher = dispatcher.Dispatcher()
     dispatcher.map("/stepTo", getOsc)
        
    

def listenOsc(ip, port):
    print("Starting Server")
    server = osc_server.ThreadingOSCUDPServer(
        (ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    

#Read the config.txt
conf = list(open("config.txt", "r"))
mode=conf[0]
csvPth=conf[1]
videoPth=conf[2]

#Read the video folder
def readFolder(videoPth):
   print(videoPth)
   videos = os.listdir(videoPth.rstrip())
   mp4_files = [_ for _ in videos if _[-4:] == ".mp4"]
   print(mp4_files)

#Read the timeline csv
def readTimeline(pthCsv):
   with open(pthCsv.rstrip(),'r') as file:
       timeline = csv.reader(file)
       timeline = list(timeline)

       count = 0
       for row in timeline:
          #print(row)
          destIp.insert(count,int(row[1]))
          stepVideo.insert(count,int(row[2]))
          count=count+1
    
   print(destIp)
   print(stepVideo)

#Start time
def config(mode):
    
   if mode >= 1:
      step = 0
      print("Master mode")
      
   else: 
      step = 0
      print("Slave mode")

#Send Osc
def sendOsc(dIp,dP,now):

   print("Ip de destino >> "+str(dIp))
   print("Puerto de destino >> "+str(dP))
   print("Play video en destino >> "+str(now))

   client = udp_client.SimpleUDPClient(dIp,dP)
   client.print_tracebacks = True
   
   client.send_message("/stepTo",now)
   time.sleep(1)
 
 #Play videos
def playVideos(vN):
    
     global playing
     
    
     print ("Dentro funcion video >> " + str(vN))
     vid = "/home/pi/Desktop/videocoto/videos/"+str(vN)+".mp4"
     print("Toca reproducir ahora: "+vid)
     
     if playing == 0:
         print("Not Playing: "+str(playing))
         VIDEO_PATH = Path(vid)
         player = OMXPlayer(VIDEO_PATH)
         player.seek(0)  
         player.play()    
         sleep(2)
         playing = 1
     
     elif playing == 1 :
        print("Is Playing: "+str(playing))
        VIDEO_PATH = Path(vid)
        player1 = OMXPlayer(VIDEO_PATH)
        player1.seek(0)  
        player1.play()    
        sleep(2)
        playing = 1
     
     
config(int(mode))
readFolder(videoPth)
readTimeline(csvPth)
listenOsc("127.0.0.1",8000)


sleep(5)
sendOsc("127.0.0.1",8000,stepVideo[2])
sleep(5)
sendOsc("127.0.0.1",8000,stepVideo[0])

  





