#import gpiozero
import numpy
import math
import logging
from logging import CRITICAL, INFO, WARNING, ERROR, DEBUG
import json
import configparser

VERSION="1.0.0"

logging.basicConfig(filename="event.log",level=INFO,format="%(levelname)s - %(asctime)s:\t%(message)s")

logging.info(f"Plakat-wechsler {VERSION}.\nCreated by Kelvin Maringer (https://www.mm-edv.at).")
logging.info("Reading Config")


#PINOUT=None
with open("config/pinout.json") as s:
    global PINOUT
    PINOUT = json.loads(s.read())
    
logging.info(f"Finished Reading config:\nPinout Version::{PINOUT['VERSION']}")
if VERSION != PINOUT["VERSION"]:
    logging.warn("Pinout version does not match Wechsler version!")











    











class Motor:
    pass





class wechsler:
    def __init__(s):
        pass
