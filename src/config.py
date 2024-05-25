import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    IMAP_SERVER = os.getenv('IMAP_SERVER')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
