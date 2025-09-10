import os
from dotenv import load_dotenv

## charger le fichier .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "super_cle_secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRES_MINUITES = int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUITES", 30))