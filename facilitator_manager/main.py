import os
import threading
from naoqi import ALProxy
import time
import sys


def worker0():
    os.system('roslaunch usb_cam usb_cam-test.launch')


def worker1():
    os.system('roslaunch multi_camera_affdex multi_camera_affdex.launch')


def worker2():
    os.system('rosbag record -a -o ../data/facilitator_HCI.bag')


t0 = threading.Thread(target=worker0)
t0.start()
threading._sleep(0.9)

# t1 = threading.Thread(target=worker1)
# t1.start()
# threading._sleep(0.9)

t2 = threading.Thread(target=worker2)
t2.start()
threading._sleep(0.2)
