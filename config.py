import os
import logging
from logging.handlers import RotatingFileHandler

# REMOVE these lines:
# from dotenv import load_dotenv
# load_dotenv()

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")  # Required
APP_ID = int(os.environ.get("APP_ID"))  # Required
API_HASH = os.environ.get("API_HASH")  # Required
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-100")) # Put a default value
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-100")) # Put a default value
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-100")) # Put a default value

# --- SET THIS CORRECTLY ---
TUTORIAL_VIDEO_ID = int(os.environ.get("TUTORIAL_VIDEO_ID", "0"))  # Default to 0, will be checked

# --- Validation ---
if not all([TG_BOT_TOKEN, APP_ID, API_HASH, CHANNEL_ID, TUTORIAL_VIDEO_ID]):
    raise ValueError("Missing required environment variables (TG_BOT_TOKEN, APP_ID, API_HASH, CHANNEL_ID, TUTORIAL_VIDEO_ID)")

print("config.py loaded successfully")
print(f"TUTORIAL_VIDEO_ID: {TUTORIAL_VIDEO_ID}, Type: {type(TUTORIAL_VIDEO_ID)}")

# NAMA OWNER
OWNER = os.environ.get("OWNER", "iBOXTVADS")

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "6124171612"))

# Port
PORT = os.environ.get("PORT", "8030")

# Database
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "bot13")

# start message
START_MSG = os.environ.get("START_MESSAGE", "<b>Hello Pirate!! {first}\n\n ɪ Store files for iBOX TV and users can access them through clicking special buttons. </b>")

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
