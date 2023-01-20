"""App configuration."""
from os import environ, getenv
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta
import random
import string

class Config:
    """Set Flask configuration vars from .env file, from docker-compose"""

    # General Config
    FLASK_DEBUG = getenv('FLASK_DEBUG','1')
    USER_DATA = getenv('USER_DATA')
    INDEX_NAME = getenv('INDEX_NAME')
    ES_DATA = getenv('ES_DATA')
    MAPPING_FILE = getenv('MAPPING_FILE')
    THRESHOLD_FILE = getenv('THRESHOLD_FILE')
    GLOSSARY_FILE = getenv('GLOSSARY_FILE')
    EXPRESSION_FILE = getenv('EXPRESSION_FILE')
    RAW_EXPRESSION_FILE = getenv('RAW_EXPRESSION_FILE')

    DST_DIR = getenv('DST_DIR')
    JSON_DIR = getenv('JSON_DIR')
    META_DIR = getenv('META_DIR')
    AUTH_DIR = getenv('AUTH_DIR')

    LOGO = getenv('LOGO', "logo.svg")
    #Authentication
    # secret_key will change whenever the backend is start if not provided
    secret_key = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    JWT_SECRET_KEY = getenv('SECRET_KEY', secret_key)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(getenv('JWT_EXPIRATION_DELTA', 10))) #10mins token expiration default
    #JWT_AUTH_HEADER_PREFIX = "JWT"
    print('Read config')
    pass
