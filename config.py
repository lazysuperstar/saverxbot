import re, os
import os
import logging
from logging.handlers import RotatingFileHandler


id_pattern = re.compile(r'^.\d+$') 

API_ID = os.environ.get("API_ID", "12936189")

API_HASH = os.environ.get("API_HASH", "7e24008e8ec33a397155b6a9d618497b")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "6396913711:AAFJpA3eMFa1Nzo9aHVGsuPys-mSocXemUY") 

FORCE_SUB = os.environ.get("FORCE_SUB", "-1001640719273") 

DB_NAME = os.environ.get("DB_NAME","Cluster0Rename")     

DB_URL = os.environ.get("DB_URL","mongodb+srv://gill1322:gill1322@cluster0rename.x8jiptm.mongodb.net/?retryWrites=true&w=majority")
 
FLOOD = int(os.environ.get("FLOOD", "10"))

START_PIC = os.environ.get("START_PIC", "")

ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1166670205').split()]

# Bot_Username = "@LazyPrincessXBOT"
BOT_USERNAME = os.environ.get("BOT_USERNAME", "@FileRenamesRobot")

PORT = os.environ.get('PORT', '8080')

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", ""))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", ""))
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", ""))

TEL_USERNAME = os.environ.get("TEL_USERNAME", "yash")
TEL_NAME = os.environ.get("TEL_NAME", "👑Yash Goyal👑")

LOG_FILE_NAME = "lazyfilelogs.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
  