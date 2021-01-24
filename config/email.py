import os
from dotenv import load_dotenv

load_dotenv()

LOGIN_EMAIL = os.getenv('LOGIN_EMAIL')
PASSWORD_EMAIL = os.getenv('PASSWORD_EMAIL')