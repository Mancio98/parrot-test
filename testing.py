import socket
import subprocess
import threading
import json
import olympe
from subprocess import Popen, PIPE
import math
import os
from sys import path

from time import sleep
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, PCMD
from olympe.messages.ardrone3.PilotingState import (
    PositionChanged,
    SpeedChanged,
    AttitudeChanged,
    AltitudeAboveGroundChanged,
    AlertStateChanged,
    FlyingStateChanged,
    NavigateHomeStateChanged,

)

from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.enums.ardrone3.PilotingState import FlyingStateChanged_State

olympe.log.update_config({"loggers": {"olympe": {"level": "WARNING"}}})

path.append(".")

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, encoding="utf8")
if __name__ == "__main__":
    IP_CLIENT = "192.168.1.14"
    run_command("gnome-terminal -- ./olympe_codes/launch_swarm.sh")
    sleep(10)
    drone = olympe.Drone("10.202.0.1")
    #sendMessage = sendMessageUpdate((IP_CLIENT, 8777))
    drone.connect()
    pdraw_drone = olympe.Pdraw()
    pdraw_drone.play(url="rtsp://10.202.0.1/live")
                                          
    sleep(5)
    run_command("gnome-terminal -- ./rtsp-simple-server")
    #sleep(2)
    #run_command("gnome-terminal -- exit -- ffmpeg -i 'rtsp://10.202.0.1/live' -crf 30 -preset ultrafast -vcodec libx264 -r 25 -b:v 500k -f rtsp 'rtsp://localhost:8554/mystream'")
    #run_command("vlc -vvv rtsp://10.202.0.1/live")
    #run_command("cvlc -vvv streamdrone.MP4 --sout '#rtp{sdp=rtsp://:8554/mylive}")
    drone(
        FlyingStateChanged(state="hovering", _policy="check")
        | FlyingStateChanged(state="flying", _policy="check")
        | (
                GPSFixStateChanged(fixed=1, _timeout=10, _policy="check_wait")
                >> (
                        TakeOff(_no_expect=True)
                        & FlyingStateChanged(
                    state="hovering", _timeout=10, _policy="check_wait")
                )
        )
    ).wait()
    #sendMessage.send({"type": "stream", "val": "true"})
    while True:
        drone(moveBy(0, 0, 20, math.pi)).wait().success()
        drone(moveBy(0, 0, -20, math.pi)).wait().success()
