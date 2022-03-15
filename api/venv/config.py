import os
from dotenv import load_dotenv

load_dotenv()

ENGLISH_API_KEY = os.getenv("ENGLISH_API_KEY")
SPANISH_API_KEY = os.getenv("SPANISH_API_KEY")
