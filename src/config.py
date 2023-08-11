from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

JWT_TOKEN = os.getenv("JVT_TOKEN")

HUNT_API_KEY = os.getenv("HUNT_API_KEY")
