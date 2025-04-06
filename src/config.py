import os

from dotenv import load_dotenv

load_dotenv()

MY_VIDEOS_PATH = os.environ.get("MY_VIDEOS_PATH")

ENC_FILE_PATH = os.environ.get("ENC_FILE_PATH")

'''
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
'''