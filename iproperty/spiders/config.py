from dotenv import load_dotenv
import os

load_dotenv()

class ENV:

    USERNAMES = os.getenv("USERNAMES")
    PASSWORDS = os.getenv("PASSWORDS")
    BASE_URL = os.getenv("BASE_URL")
    SEARCH_URL = os.getenv("SEARCH_URL")
