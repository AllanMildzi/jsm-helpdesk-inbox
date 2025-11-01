import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from utils import get_logger
from imap_client import EmailListener
from core import Config

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

if __name__ == "__main__":
    uvicorn.run(app, host=Config.SERVER_HOST, port=Config.SERVER_PORT)