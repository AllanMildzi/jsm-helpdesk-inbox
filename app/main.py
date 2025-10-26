import logging
import uvicorn
from fastapi import FastAPI

from imap_client import EmailListener
from core import Config

logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI server running with IMAP listener"}

@app.on_event("startup")
def startup_event():
    logging.basicConfig(filename='logger.log', level=logging.INFO)

    print("Starting IMAP email listener...")
    print("Running in:", Config.ENV)
    print("Debug mode:", Config.DEBUG)

    listener = EmailListener(Config.IMAP_HOST, Config.USERNAME, Config.APP_PASSWORD)
    listener.start()

if __name__ == "__main__":
    uvicorn.run(app, host=Config.SERVER_HOST, port=Config.SERVER_PORT)