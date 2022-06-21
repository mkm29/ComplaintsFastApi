import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(ROOT_DIR, "temp_files")
CHARSET = "UTF-8"
FROM_EMAIL = "noreply@smigula.com"
