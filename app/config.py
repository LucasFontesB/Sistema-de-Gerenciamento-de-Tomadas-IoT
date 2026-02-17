import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_PATH = "dispositivos.db"
    STATUS_INTERVAL = 5
    SOCKET_TIMEOUT = 2

    SECRET_KEY = os.environ.get("SECRET_KEY")