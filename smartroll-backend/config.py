import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLASS_WIFI_SUBNETS = [s.strip() for s in os.getenv("CLASS_WIFI_SUBNETS", "10.").split(",")]
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "smartroll-admin-123")
