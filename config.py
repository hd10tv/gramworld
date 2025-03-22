import os
import logging
from logging.handlers import RotatingFileHandler

# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "5166878"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "fdafb41f9a67f40e34a6c67f47730a92")

# Your DB channel ID
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001973418807"))

# Bot owner username
OWNER = os.environ.get("OWNER", "iBOXTVADS")

# Owner ID
OWNER_ID = int(os.environ.get("OWNER_ID", "6124171612"))

# Port
PORT = os.environ.get("PORT", "8030")

# Database
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "bot13")

# Force subscription channel IDs
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002311266823"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1002311266823"))

# Number of workers for the bot
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Start message
START_MSG = os.environ.get(
    "START_MESSAGE",
    "<b>Hello Pirate!! {first}\n\n I store files for iBOX TV, and users can access them by clicking special buttons.</b>"
)

# Admins
try:
    ADMINS = [6124171612]
    for x in os.environ.get("ADMINS", "762308466").split():
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

# Force subscription message
FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE",
    "ʜᴇʟʟᴏ {first}\n\n<b>ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ using any button below ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ꜰɪʟᴇ.</b>"
)

# Custom caption (set to None to disable)
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# Prevent users from forwarding files
PROTECT_CONTENT = os.environ.get("PROTECT_CONTENT", "False") == "True"

# Disable channel post share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False") == "True"

# Tutorial video file ID
TUTORIAL_VIDEO_ID = os.environ.get("TUTORIAL_VIDEO_ID", "")

# Bot statistics text
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"

# Unauthorized user response
USER_REPLY_TEXT = "Pirate! ʏᴏᴜ need to be my owner to do that!!"

# Add owner and admin IDs
ADMINS.append(OWNER_ID)
ADMINS.append(6124171612)

# Logging setup
LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
