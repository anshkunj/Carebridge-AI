import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super_jwt_secret")

    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")

    MEDICAL_DISCLAIMER = (
        "This AI tool is for informational purposes only and "
        "does not replace professional medical advice."
    )