#Plakat wechsler, Created by:
#   Kelvin Maringer (https://www.mm-edv.at)
VERSION="1.0.0"

import logging
logging.basicConfig(filename="event.log",level=logging.DEBUG,format="%(levelname)-8s - %(asctime)s [%(filename)-15s|%(lineno)4d]:\t%(message)s",filemode="w+")
logging.info(f"Plakat-wechsler {VERSION}.")
logging.info(f"Created by Kelvin Maringer (https://www.mm-edv.at).")
logging.info("_"*60)


#imports
import RPi.GPIO as gz
gz.setmode(gz.BCM)
from PLAKAT_WECHSLER import *
from PLAKAT_WECHSLER.flows.EStop import E_STOP
import json
import traceback



Presenters=[]

if __name__ == "__main__":
    try:
        logging.info("Reading Config...")

        with open("config/pinout.json") as s:
            global PINOUT
            PINOUT = json.loads(s.read())

        config = configparser.ConfigParser()
        config.read("config/config.ini")

        logging.info(f"Finished Reading configs.")
        logging.info(f"Pinout Version::{PINOUT['VERSION']}")
        
        Door=Sensor(PINOUT["Door.DPin"])


        for x in PINOUT["Presenters"]:
            MDP=x["Motor"]
            Mot = Motor(MDP["DPinR"],MDP["DPinL"],MDP["Ind_UP.DPin"],MDP["Ind_DOWN.DPin"])
            Light = Actor(x["Light.DPin"])
            MDP=x["LightSens"]
            LightSens = LightSensor(MDP["maxL"],MDP["minL"],MDP["APin"],config["LIGHT"]["LightThreashhold"])

            Presenters.append(WECHSLER(Mot,Door,LightSens,Light))

        
    except Exception as expt:
        logging.critical(f"Unhandled exception occured!:\n{traceback.format_exc()}")
        E_STOP()
        exit()
        
else:
    logging.error("Second process unexpectedly opened!")

logging.critical("EOF")
