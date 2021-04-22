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

#global
step = 0
now = 0
play = False
destPort = 0
portIn = 8000
destIp = array('i')
stepVideo = array('l')


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

#Start time
def config(mode):
    
   if mode >= 1:
      step = 0
      print("Master mode")
      
   else: 
      step = 0
      print("Slave mode")

#Send Osc
def sendOsc(destIp,destPort,now):

   finalIp = "192.168.200."+str(destIp)
   print("Ip de destino>> "+str(finalIp))
   print("Puerto de destino>> "+str(destPort))
   print("Play video en destino>> "+str(now))

   client = udp_client.SimpleUDPClient(finalIp,destPort)
   
   client.send_message("/stepTo",now)
   time.sleep(1)
   
#Receive Osc
def recOsc():
     print("Msg")
      
#Display videos
def playVideos():
     #sleep(5)
     player = OMXPlayer(videoNow)
     player.play()
     player.quit()


readFolder(videoPth)
readTimeline(csvPth)
config(int(mode))
#sendOsc(destIp[0],destPort,now)

print(destIp);
print(stepVideo);


    





