import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SHORTENED_URLS_STORAGE_FILEPATH = BASE_DIR / "shortened_urls.json"

LOG_LEVEL = logging.INFO

LOG_FORMAT = str(
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

USERS_DB: dict[str, str] = {
    # username: password
    "bob": "qwerty",
    "admin": "admin",
}


REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2

REDIS_TOKENS_SET_NAME = "tokens"
