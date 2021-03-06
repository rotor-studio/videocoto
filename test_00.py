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
import threading
from pythonosc import dispatcher
from pythonosc import osc_server


#global
step = 0
now = 0
play = False
destPort = 8000
portIn = 8000
listenIp = "127.0.0.1"
destIp = array('i')
stepVideo = array('l')
timeVideo = array('l')
videoNow = " "
vidNow = 0
playing = 0
totalSteps = 0
slave = 0
omx_arg = ['--no-osd', '-b','--loop']
omx_arg_pasive = ['--no-osd','-b']
#omx_arg = ['--timeout', '2000', '--live', '--blank', '--refresh', '--no-keys']	
bus = ["org.mpris.MediaPlayer2.omxplayer1" ,"org.mpris.MediaPlayer2.omxplayer2",]

#player = OMXPlayer("/home/pi/Desktop/videocoto/videos/0.mp4", args=omx_arg, dbus_name = bus[0])
#player1 = OMXPlayer("/home/pi/Desktop/videocoto/videos/1.mp4", args=omx_arg, dbus_name = bus[1])

start = False
first = 0

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
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    

#Read the config.txt
conf = list(open("config.txt", "r"))
mode=conf[0]
csvPth=conf[1]
videoPth=conf[2]
listenIp = conf[3]
portIn = conf[4]
destPort = conf[5]


#Read the video folder
def readFolder(videoPth):
   print(videoPth)
   videos = os.listdir(videoPth.rstrip())
   mp4_files = [_ for _ in videos if _[-4:] == ".mp4"]
   print(mp4_files)
   
   if slave == True:
       totalSteps = len(mp4_files)
       print("Numero de v??deos en la carpeta: " + str(totalSteps))

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
          timeVideo.insert(count,int(row[3]))
          count=count+1
          
          global totalSteps
          totalSteps = count
    
   print(destIp)
   print(stepVideo)
   print(timeVideo)
   print("Numero de pasos en la secuencia: " + str(totalSteps))

#Start time
def config(mode):
   
   global start
   global slave
   
   if start == False:
       if mode == 1:
          print("Master mode")
          slave = False
          readFolder(videoPth)
          readTimeline(csvPth)
          listenOsc("192.168.0.103",8000)
          start=True
     
       elif mode == 0: 
          print("Slave mode")
          slave = True
          readFolder(videoPth)
          listenOsc("192.168.0.103",8000)
          start=True

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
     global player
     global player1
     global first
     
     print ("Dentro funcion video >> " + str(vN))
     vid = "/home/pi/Desktop/videocoto/videos/"+str(vN)+".mp4"
     print("Toca reproducir ahora: "+vid)
      
     if playing == 0:
         print("Not Playing: "+str(playing))
         
         VIDEO_PATH = Path(vid)
         if slave == False:
              player = OMXPlayer(VIDEO_PATH, args=omx_arg, dbus_name = bus[0])
              
         
         if slave == True:
              player = OMXPlayer(VIDEO_PATH, args=omx_arg_pasive, dbus_name = bus[0])
              
         
         
         player.seek(0)  
         player.play()
         
         
         if first == 1:
            player1.stop()
             
         first = 1
         playing = 1
         
     
     elif playing == 1 :
        print("Is Playing: "+str(playing))
        
        VIDEO_PATH = Path(vid)
        if slave == False :
              player1 = OMXPlayer(VIDEO_PATH, args=omx_arg, dbus_name = bus[1])
              
         
        if slave == True:
              player1 = OMXPlayer(VIDEO_PATH, args=omx_arg_pasive, dbus_name = bus[1])
              
              
        player1.seek(0)  
        player1.play()
        
        
        player.stop()
        playing = 0

    
        
#Previene de falsos apagados
def patch_OMXPLayer_quit():
    old_quit = OMXPlayer.quit
    def new_quit(self):
        self._connection._bus.close()
        old_quit(self)
    OMXPlayer.quit = new_quit
patch_OMXPLayer_quit()

def startSec(init, tSteps):
    
    if init == True:
        
        i = 0
        while i <= tSteps:
           i = i+1
           print("Paso ahora > "+str(i-1)+" de "+str(tSteps))
           time.sleep(timeVideo[i-1])
           sendOsc("192.168.0."+str(destIp[i-1]),int(destPort),stepVideo[i-1])

           
           if i == tSteps:
               print("start again")
               i = 0
           
              
              
config(int(mode))

#Se activa si hay Master
if slave == False:
    startSec(start, totalSteps)




    
    

   

  







