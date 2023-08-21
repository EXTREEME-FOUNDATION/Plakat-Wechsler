#import gpiozero
import numpy
import math
import logging
import json
import configparser
import multiprocessing
import signal
from types import FunctionType

# IMPORT flows
from PLAKAT_WECHSLER.flows import EStop

from time import sleep


config = configparser.ConfigParser()
config.read("config/config.ini")

                    
def MAXTIME(time:int=config["SAFETY"].getint("Shutofftime")) -> FunctionType:
    """Limits time a function can take, returns TimeoutError if time has elapsed
    -> if out:=decorated_function() == TimeoutError:"""
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



class Safety:
    """implements different safety features into other classes"""
    def E_STOP(s,msg=None):
        logging.critical(f"E-STOP TRIGGERED in <{s}> with error msg: \"{msg}\"")
        EStop.E_STOP()


class LightSensor:
    def __init__(s,maxL:float,minL:float,APin:int,Activval:float):
        """maxL: maximum value of PRS
        minL: minimum value of PRS
        Activval: relative value at which the sensor is activated"""
        s.Value=0.0
        s.normvals=(maxL,minL)
        s.APin=APin
        testok = s.update()

    def update(s) -> float:
        #Code to read sensor
        s.Value = 0.5
        return 0.5
    def __float__(s) -> float:
        return s.Value
    
class Sensor:
    def __init__(s,DPin):
        s.State=False
        s.Dpin=DPin
        testok = s.update()
    def update(s) -> bool:
        #Code to read sensor
        s.State=False
        return False
    def __int__(s) -> bool:
        return s.State







class Motor(Safety):
    def __init__(s,RPin:int,LPin:int,SensU:Sensor,SensD:Sensor) -> False:
        """SensU: end-sensor | SensD: sensor for poster halt"""
        s.R=RPin
        s.L=LPin
        s.Direction=0# 0:off/brake | 1: clockwise | -1: counterclockwise
        s.Poster=0 #What poster is beeing shown

        #MAKE FUNCTION TO NULL DEVICE (get current poster)
        pass
    @MAXTIME()
    def __ToRight(s):
        #ONLY USE THIS FUNCTION IF TIMEOUTERROR IS HANDLED!!!
        #CAN CAUSE DEVICE DAMAGE IF NOT CORRECTLY ADRESSED
        #drive to right
        sleep(5)
        pass
    @MAXTIME()
    def __ToLeft(s):
        #ONLY USE THIS FUNCTION IF TIMEOUTERROR IS HANDLED!!!
        #CAN CAUSE DEVICE DAMAGE IF NOT CORRECTLY ADRESSED
        #drive to left
        pass
    @MAXTIME(time=1)
    def __Stop(s):
        #ONLY USE THIS FUNCTION IF TIMEOUTERROR IS HANDLED!!!
        #CAN CAUSE DEVICE DAMAGE IF NOT CORRECTLY ADRESSED
        #stop
        pass
    def ToPosterNum(s,num):
        #drive to poster number
        while(1):
            if num < s.Poster:
                print("driving to left")
                if s.__ToLeft() == TimeoutError:
                    s.E_STOP("Timeout while Driving motor to Left")
                    #Possible __ToRight() implementation
            elif num > s.Poster:
                print("driving to right")
                if s.__ToRight() == TimeoutError:
                    s.E_STOP("Timeout while Driving motor to Left")
            else:
                print("Reached destination")
                if s.__Stop() == TimeoutError:
                    s.E_STOP("Timeout while Stopping")
                break
    def __str__(s):
        return f"Motor@Pin{s.R} and Pin{s.L}"

