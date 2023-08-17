#Plakat wechsler, Created by:
#   Kelvin Maringer (https://www.mm-edv.at)
import logging
logging.basicConfig(filename="event.log",level=logging.INFO,format="%(levelname)s - %(asctime)s:\t%(message)s")
from PLAKAT_WECHSLER.flows.EStop import E_STOP
#imports

import json
VERSION="1.0.0"





if __name__ == "__main__":
    try:
        import PLAKAT_WECHSLER
    except Exception as expt:
        logging.critical(f"Unhandled exception occured!:\n{expt}")
        E_STOP()
        exit()
        
else:
    logging.error("Second process unexpectedly opened!")


