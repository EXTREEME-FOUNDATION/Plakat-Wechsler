#Plakat wechsler, Created by:
#   Kelvin Maringer (https://www.mm-edv.at)
VERSION="1.0.0"

import logging
logging.basicConfig(filename="event.log",level=logging.DEBUG,format="%(levelname)-8s - %(asctime)s [%(filename)-15s|%(lineno)4d]:\t%(message)s",filemode="w+")
logging.info(f"Plakat-wechsler {VERSION}.")
logging.info(f"Created by Kelvin Maringer (https://www.mm-edv.at).")
logging.info("_"*60)


#imports
from PLAKAT_WECHSLER import *
from PLAKAT_WECHSLER.flows.EStop import E_STOP
import json
import traceback




Motors=[]

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
        
        for x in PINOUT["Motors"]:
            Motors.append(Motor(x["DpinR"],x["DpinL"],Sensor(x["Ind_UP.Dpin"]),Sensor(x["Ind_DOWN.Dpin"])))
            logging.debug(Motors[-1])

        logging.info(f"{len(Motors)} Motors connected to Terminal")

        
        Lsens = LightSensor(PINOUT["Sensor"]["light"][0]["maxL"],PINOUT["Sensor"]["light"][0]["minL"],PINOUT["Sensor"]["light"][0]["Apin"],config["LIGHT"]["LightThreashhold"])
        logging.info(f"1 Light Sensor@Pin{Lsens.APin} active")

        Opne = Sensor(PINOUT["Sensor"]["other"][0][0]) # PARRALELL SWITCH


        Motors[0].ToPosterNum(2)
    except Exception as expt:
        logging.critical(f"Unhandled exception occured!:\n{traceback.format_exc()}")
        E_STOP()
        exit()
        
else:
    logging.error("Second process unexpectedly opened!")

logging.critical("EOF")
