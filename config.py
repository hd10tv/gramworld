import os
import logging
from logging.handlers import RotatingFileHandler

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = os.environ.get("APP_ID", "")  # Get as string initially
API_HASH = os.environ.get("API_HASH", "")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001973418807"))
OWNER = os.environ.get("OWNER", "iBOXTVADS")
OWNER_ID = int(os.environ.get("OWNER_ID", "6124171612"))
PORT = os.environ.get("PORT", "8030")
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "bot13")
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002311266823"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1002311266823"))
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
START_MSG = os.environ.get("START_MESSAGE", "<b>Hello Pirate!! {first}\n\n ɪ Store files for iBOX TV and users can access them through clicking special buttons. </b>")

# --- Add TUTORIAL_VIDEO_ID ---
TUTORIAL_VIDEO_ID = os.environ.get("TUTORIAL_VIDEO_ID", "0")  # Get as string, default "0"

try:
    ADMINS=[6124171612]
    for x in (os.environ.get("ADMINS", "762308466").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "ʜᴇʟʟᴏ {first}\n\n<b>ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ using any button below ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ꜰɪʟᴇ.</b>")
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False
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

# --- Validation and Conversion ---
if not TG_BOT_TOKEN:
    raise ValueError("TG_BOT_TOKEN environment variable is not set.")
if not APP_ID:
    raise ValueError("APP_ID environment variable is not set.")
if not API_HASH:
    raise ValueError("API_HASH environment variable is not set.")
if not TUTORIAL_VIDEO_ID or TUTORIAL_VIDEO_ID == "0":
    raise ValueError("TUTORIAL_VIDEO_ID environment variable is not set or is set to '0'.")

try:
    APP_ID = int(APP_ID)  # Convert to integer *after* checking if it exists
except (ValueError, TypeError) as e:
    raise ValueError(f"APP_ID environment variable must be a valid integer. Error: {e}")

try:
    TUTORIAL_VIDEO_ID = int(TUTORIAL_VIDEO_ID) # Convert to int *after* check
except (ValueError, TypeError) as e:
     raise ValueError(f"TUTORIAL_VIDEO_ID environment variable must be a valid integer. Error: {e}")

print("config.py loaded successfully")
print(f"TUTORIAL_VIDEO_ID: {TUTORIAL_VIDEO_ID}, Type: {type(TUTORIAL_VIDEO_ID)}")


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
