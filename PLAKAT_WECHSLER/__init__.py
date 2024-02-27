import RPi.GPIO as gz
import numpy # has no implementation in this context!
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


#       message broadcast with system -> linux broadcast safe?
#       Sigtimer safe?
#       implement IO sub-program handling input for the device
#       implement system checks for IOSP & dissable internet/unknown services -> minimizes interruptions
#       start Proc with nice specifier
#       save last version for backup
#       over the air update with BLE module
#       OTA has to be Fail-Safe.
#       implement checks for the config file data -> use standard config / dissable afflicted parts -> shutdown should be the last resort!










config = configparser.ConfigParser()
config.read("config/config.ini")

                    
def MAXTIME(time:int=config["SAFETY"].getint("Shutofftime")) -> FunctionType:# All time-critical functions should be appended to IO Thread, not handled by unsupervised programm without routine checks.
    """Limits time a function can take, returns TimeoutError if time has elapsed
    -> if out:=decorated_function() == TimeoutError:"""
    def ovrdecorator(func):
        def hwlp(sig,frame):
            raise TimeoutError
        def wrapper(*args, **kwargs) -> any:
            signal.signal(signal.SIGALRM,hwlp)
            signal.alarm(time)# Thrustworthy? is this systemfeature safe for use in time critical application?
            try:
                out = func(*args,**kwargs)
                return out
            except TimeoutError:
                logging.warn(f"Function \"{func.__name__}\" took to long to execute. ({time}s)")#logging should be global instead of local -> return
                return TimeoutError
        return wrapper
    return ovrdecorator



class Safety:# failsafe implements shuld only be handled by IO Thread!
    """implements different safety features into other classes"""
    def E_STOP(s,msg=None):
        logging.critical(f"E-STOP TRIGGERED in <{s}> with error msg: \"{msg}\"")
        EStop.E_STOP()
    def Retsave(s,lastpos,msg=None):
        logging.error(f"TestSave Triggerred in <{s}> with error msg: \"{msg}\"")


class Actor:# Actor should be more genral, only used by motor (maybe group Actor, Sensor and LSenscon)
    state:bool=False
    def __init__(s,Dpin:int):
        s.DPin:int=Dpin
        gz.setup(s.DPin,gz.OUT)
    def Switch(s):
        if s.state: s.off()
        else: s.on()
    def on(s):
        s.tostate(True)
    def off(s):
        s.tostate(False)
    def tostate(s,state:bool):
        gz.output(s.DPin,state)
        s.state:bool= state


class LightSensor:
    def __init__(s,maxL:float,minL:float,APin:int,Activval:float):
        """maxL: maximum value of PRS
        minL: minimum value of PRS
        Activval: relative value at which the sensor is activated"""
        s.Value=0.0
        s.normvals=(maxL,minL)
        s.APin=APin
        testok = s.update()

    def update(s) -> float:# update in check -> append to IO thead/multiprocessing child -> build failsafe arcitecture, message broadcast between programms, build IO Prog. in different, compilable language!
        #Code to read sensor
        s.Value = 0.5
        return s.Value
    def __float__(s) -> float:
        return s.Value
    
class Sensor:# sensor braucht failsafe -> kontinuierlicher check, routine check!!!!!!!!!
    def __init__(s,DPin):
        s.State=False
        s.Dpin=DPin
        testok = s.update()
    def update(s) -> bool:
        #Code to read sensor
        s.State=False
        return s.State
    def __int__(s) -> bool:
        return s.State







class Motor(Safety):
    def __init__(s,RPin:int,LPin:int,SensU:Sensor,SensD:Sensor) -> False:
        """SensU: end-sensor | SensD: sensor for poster halt"""
        s.R=Actor(RPin)#Actor class is kind of pointless in this usecase -> use as template instead
        s.L=Actor(LPin)
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
    @MAXTIME(time=1)#time in ms or in s? CHECK & Documentation
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
                if s.__ToLeft() == TimeoutError:# if handling check! possible to do in a batch (repetition)
                    s.E_STOP("Timeout while Driving motor to Left")# kein e-stop, checkback
                    #Possible __ToRight() implementation
            elif num > s.Poster:
                print("driving to right")
                if s.__ToRight() == TimeoutError:
                    s.E_STOP("Timeout while Driving motor to Left")
            else:
                print("Reached destination")
                if s.__Stop() == TimeoutError:
                    s.E_STOP("Timeout while Stopping")# this is a critical funktion, disconnect power immediatly!!!!
                break
    def __str__(s):
        return f"Motor@Pin{s.R.DPin} and Pin{s.L.DPin}"


class WECHSLER(Safety):#init mit motorconfig anstelle von jedem object einzeln. Surface level soll nur befehle ans objekt schicken!
    """takes all input classes and puts them in an easy to access class.
    1 class instance represents 1 side of the Presenter"""
    def __init__(s,Motor:Motor,open:Sensor,Lightsens:LightSensor=None,Light:Actor=None):#implement mit wechsler E-stop und fallback, KEIN UNDEFINIERTER STATUS!!!!!!!
        pass


