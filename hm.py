import os
from urllib.parse import quote_plus

MONGO_USERNAME = os.getenv("MONGO_USERNAME", "asifnawazaddy")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "nL6SFfp4Af8ckocZ")
DB_NAME = os.getenv("DB_NAME", "local_pdf_db")

# URL-encode password to avoid special character issues
encoded_password = quote_plus(MONGO_PASSWORD)

MONGO_URI = (
    f"mongodb+srv://{MONGO_USERNAME}:{encoded_password}@cluster0.5fv3e.mongodb.net/{DB_NAME}"
    "?retryWrites=true&w=majority&tls=true&tlsVersion=TLS1_2&tlsAllowInvalidCertificates=true&appName=Cluster0"
)

print("MongoDB URI:", MONGO_URI)  # Remove this after testing
