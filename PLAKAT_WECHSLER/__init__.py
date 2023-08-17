#import gpiozero
import numpy
import math
import logging
from logging import CRITICAL, INFO, WARNING, ERROR, DEBUG
import json
import configparser
import multiprocessing
import signal
from types import FunctionType

# IMPORT flows
from PLAKAT_WECHSLER.flows import getstatus
from PLAKAT_WECHSLER.flows import selftest
from PLAKAT_WECHSLER.flows import update
from PLAKAT_WECHSLER.flows import webserv


from time import sleep

VERSION="1.0.0"


logging.info(f"Plakat-wechsler {VERSION}.\nCreated by Kelvin Maringer (https://www.mm-edv.at).")
logging.info("Reading Config")


#PINOUT=None
with open("config/pinout.json") as s:
    global PINOUT
    PINOUT = json.loads(s.read())

config = configparser.ConfigParser()
config.read("config/config.ini")



logging.info(f"Finished Reading configs:\nPinout Version::{PINOUT['VERSION']}")


                    
def MAXTIME(time:int=config["SAFETY"]["Shutofftime"]) -> FunctionType:
    """Limits time a function can take"""
    def ovrdecorator(func):
        def hwlp(sig,frame):
            raise TimeoutError
        def wrapper(*args, **kwargs) -> any:
            signal.signal(signal.SIGALRM,hwlp)
            signal.alarm(time)
            try:
                out = func(*args,**kwargs)
                return out
            except TimeoutError:
                logging.warn(f"Function \"{func.__name__}\" took to long to execute. ({time}s)")
                return TimeoutError
        return wrapper
    return ovrdecorator




class LightSensor:
    def __init__(s,maxL,minL,APin) -> bool:
        s.Value=0.0
        s.normvals=(maxL,minL)
        s.APin=APin
        testok = s.update()
        if testok in (0.0,1.0):
            logging.error(f"Light sensor defective, value of {testok}")
            return False
        return True

    def update(s) -> float:
        #Code to read sensor
        s.Value = 0.5
        return 0.5
    def __float__(s) -> float:
        return s.Value
    
class Sensor:
    def __init__(s,DPin) -> bool:
        s.State=False
        s.Dpin=DPin
        testok = s.update()
    def update(s) -> bool:
        #Code to read sensor
        s.State=False
        return False
    def __int__(s) -> bool:
        return s.State







class Motor:
    def __init__(s,RPin,LPin,SensU,SensD) -> False:
        s.R=RPin
        s.L=LPin
        s.Direction=0# 0:off/brake | 1: clockwise | -1: counterclockwise
        s.Poster=0 #What poster is beeing shown
        pass
    @MAXTIME()
    def __ToRight(s):
        #drive to right
        pass
    @MAXTIME()
    def __ToLeft(s):
        #drive to left
        pass
    @MAXTIME(time=1)
    def __Stop(s):
        #stop
        pass
    def ToPosterNum(s,num):
        #drive to poster number
        while(1):
            if num < s.Poster:
                if s.ToLeft() == TimeoutError:
                    s.Stop()
            elif num > s.Poster:
                s.ToRight()
            else:
                s.Stop()
                break
print("finished running")
sleep(20)
print("EOF")