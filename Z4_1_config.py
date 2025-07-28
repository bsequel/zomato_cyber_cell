
import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


DB_CONFIG = {
    "dbname": "Zomato",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}

PDF_PASSWORD = "Zomato@123"

GMAIL_APP_PASSSWORD = os.getenv('App_Password')


EMAIL_SETTINGS = {
    'from': 'beginasnoob1996@gmail.com',
    'to': 'bheem.singh2827@gmail.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'smtp_user': 'beginasnoob1996@gmail.com',
    'smtp_password': GMAIL_APP_PASSSWORD
}