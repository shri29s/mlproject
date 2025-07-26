from waitress import serve
from app import app
import os

serve(app=app, host="0.0.0.0", port=os.getenv("PORT", 8080))