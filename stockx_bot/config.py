import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
SUPPORT_TG = os.getenv("SUPPORT_TG", "")

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB_FILE = BASE_DIR / "db.sqlite3"
TEMPLATES_DIR = BASE_DIR / "templates"
GOOGLE_SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_ID", "")

ADMIN_IDS = [int(admin_id) for admin_id in os.getenv("ADMIN_IDS").split(",")]
DEVELOPER_CHAT_ID = ADMIN_IDS[0]
MANAGER_CHAT_ID = ADMIN_IDS[1]
NOTIFY_ADMIN_ON_ERROR = False
DATE_FORMAT = "%d.%m.%Y"


EVENT_START = "events"

LOG_FILE_NAME = "./logs/bot.log"
TZ = "Europe/Moscow"
