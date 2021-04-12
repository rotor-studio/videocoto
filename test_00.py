from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)


VIDEO_PATH = Path("/home/pi/Desktop/test.h264")
player_log = logging.getLogger("Video 1")

player = OMXPlayer(VIDEO_PATH)


sleep(5)

player.play()

sleep(5)

