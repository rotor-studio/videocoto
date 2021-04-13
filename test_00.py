from pathlib import Path
from time import sleep
import time
from random import shuffle
from glob import glob
from glob import iglob
import os
import csv
from omxplayer.player import OMXPlayer
import logging
logging.basicConfig(level=logging.INFO)
from pythonosc.udp_client import SimpleUDPClient
from array import *

#global
step = 0
now = 2
play = False
destPort = array('i')
destIp = "localhost"
stepVideo = array('l')



#Read the config.txt
conf = list(open("config.txt", "r"))
mode=conf[0]
csvPth=conf[1]
videoPth=conf[2]

#Read the video folder
def readFolder(videoPth):
   videos = [file_path for _, _, file_path in os.walk(videoPth)]
   for file_name in videos[0]:
      print(file_name)

#Read the timeline csv
def readTimeline(pthCsv):
   with open(pthCsv.rstrip(),'r') as file:
       timeline = csv.reader(file)
       timeline = list(timeline)

       count = 0
       for row in timeline:
          #print(row)
          destPort.insert(count,int(row[1]))
          stepVideo.insert(count,int(row[2]))
          count =+ 1

#Start time
def config(mode):
    
   if mode >= 1:
      step = 0
      print("Master mode")
      
   else: 
      step = 0
      print("Slave mode")
      
#Display videos
def playVideos():
     #sleep(5)
     player = OMXPlayer(videoNow)
     player.play()
     player.quit()


readFolder(videoPth)
readTimeline(csvPth)
config(int(mode))

print(destPort);
print(stepVideo);


    





