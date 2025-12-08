from fastapi import FastAPI
from contextlib import asynccontextmanager

from utils import get_logger
from imap_client import EmailListener
from core import Config
from gmail import Gmail

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting IMAP email listener...")
    logger.info(f"Running in: {Config.ENV}")
    logger.info(f"Debug mode: {Config.DEBUG}")

    listener = EmailListener(Config.IMAP_HOST, Config.USERNAME, Config.APP_PASSWORD)
    listener.start()
    yield
    listener.stop()

app = FastAPI(lifespan=lifespan)

@app.get("/authenticate")
async def root():
    Gmail.generate_token()
    
    return {"message": "Token generated"}