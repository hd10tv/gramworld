import os
import logging
from logging.handlers import RotatingFileHandler

# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "5166878"))  # Replace with a default or raise an error

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "fdafb41f9a67f40e34a6c67f47730a92") # Replace with a default

# Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001973418807"))

# NAMA OWNER
OWNER = os.environ.get("OWNER", "iBOXTVADS")

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "6124171612"))

# Port
PORT = os.environ.get("PORT", "8030")

# Database
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "bot13")

# force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002311266823"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1002311266823"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# start message
START_MSG = os.environ.get("START_MESSAGE", "<b>Hello Pirate!! {first}\n\n ɪ Store files for iBOX TV and users can access them through clicking special buttons. </b>")

# Tutorial Video Message ID (from your private channel) -  MAKE SURE THIS IS AN INTEGER!
TUTORIAL_VIDEO_ID = int(os.environ.get("TUTORIAL_VIDEO_ID", "0"))  # Default to 0, raise error later if it's 0

try:
    ADMINS = [6124171612]
    for x in (os.environ.get("ADMINS", "762308466").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

# Force sub message
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "ʜᴇʟʟᴏ {first}\n\n<b>ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ using any button below ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ꜰɪʟᴇ.</b>")

# set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "Pirate ! ʏᴏᴜ Need to be myy Owner to do that !!"

ADMINS.append(OWNER_ID)
ADMINS.append(6124171612)

LOG_FILE_NAME = "filesharingbot.txt"

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

# --- Validation Check for TUTORIAL_VIDEO_ID ---
if TUTORIAL_VIDEO_ID == 0:
    raise ValueError("TUTORIAL_VIDEO_ID must be set to a valid message ID (a non-zero integer) in your environment variables.")
